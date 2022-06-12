from django.db import transaction, DatabaseError
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from tzapp.models.elements.name_element import NameElement
from tzapp.models.elements.address_element import AddressElement
from tzapp.models.form import Form

from .serializers import NameElementSerializer, AddressElementSerializer


element_serializer_map = {
    'name': NameElementSerializer,
    'address': AddressElementSerializer
}

element_model_map = {
    'name': NameElement,
    'address': AddressElement
}


class ElementCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)
            element = request.query_params.get('element', None)
            position = request.query_params.get('position', None)

            if not element:
                return Response(data={'detail': 'Please provide element type'}, status=status.HTTP_400_BAD_REQUEST)

            if not position:
                return Response(data={'detail': 'Please provide element position'}, status=status.HTTP_400_BAD_REQUEST)

            ElementSerializer = element_serializer_map.get(element, None)
            ElementModel = element_model_map.get(element, None)

            if not ElementSerializer:
                return Response(data={'detail': 'Element type not found'}, status=status.HTTP_404_NOT_FOUND)

            if not ElementModel:
                return Response(data={'detail': 'Element type not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ElementSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data={'detail': 'Invalid element input', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    new_element = ElementModel(**serializer.data, form=form)
                    new_element.save()

                    order = form.order
                    if order:
                        order.insert(int(position), {'element_type': element, 'element_id': str(new_element.id)})
                    else:
                        order.append({'element_type': element, 'element_id': str(new_element.id)})

                    form.order = order
                    form.save()
            except DatabaseError:
                return Response(data={'detail': 'Database error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            new_serializer = ElementSerializer(instance=new_element)
            return Response(data={'detail': 'Element created', 'element': new_serializer.data, 'order': order}, status=status.HTTP_201_CREATED)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)


class ElementDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, form_id, pk):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)

            element = request.query_params.get('element', None)
            if not element:
                return Response(data={'detail': 'Please provide element type'}, status=status.HTTP_400_BAD_REQUEST)

            ElementModel = element_model_map.get(element, None)
            ElementSerializer = element_serializer_map.get(element, None)

            try:
                existing_element = ElementModel.objects.get(pk=pk, form=form)
                serializer = ElementSerializer(instance=existing_element)

                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except ElementModel.DoesNotExist:
                return Response(data={'detail': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)

        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, form_id, pk):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)

            element = request.query_params.get('element', None)
            if not element:
                return Response(data={'detail': 'Please provide element type'}, status=status.HTTP_400_BAD_REQUEST)

            ElementModel = element_model_map.get(element, None)
            ElementSerializer = element_serializer_map.get(element, None)

            try:
                existing_element = ElementModel.objects.get(pk=pk, form=form)
                serializer = ElementSerializer(instance=existing_element, data=request.data)

                if not serializer.is_valid():
                    return Response(data={'detail': 'Invalid input details', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except ElementModel.DoesNotExist:
                return Response(data={'detail': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)

        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, form_id, pk):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)

            element = request.query_params.get('element', None)
            if not element:
                return Response(data={'detail': 'Please provide element type'}, status=status.HTTP_400_BAD_REQUEST)

            ElementModel = element_model_map.get(element, None)

            try:
                existing_element = ElementModel.objects.get(pk=pk, form=form)

                try:
                    with transaction.atomic():
                        form.order = list(filter(lambda i: i['element_id'] != str(existing_element.id), form.order))
                        form.save()
                        existing_element.delete()

                        return Response(data={'detail': 'Element Deleted'}, status=status.HTTP_204_NO_CONTENT)
                except DatabaseError:
                    return Response(data={'detail': 'Database error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ElementModel.DoesNotExist:
                return Response(data={'detail': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)

        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)
