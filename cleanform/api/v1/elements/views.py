from django.db import transaction, DatabaseError
from rest_framework import serializers, generics, permissions, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from cleanform.models.form import Form
from cleanform.models.element import Element


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            'id',
            'label',
            'description',
            'is_required',
            'type',
            'properties',
            'layouts'
        ]


class ElementListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)
            elements = Element.objects.filter(form=form)

            element_serializer = ElementSerializer(elements, many=True)
            return Response(data=element_serializer.data, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, form_id):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)
            element_serializer = ElementSerializer(data=request.data)

            if not form.elements:
                form.elements = []
                default_position = 0
            else:
                default_position = len(form.elements)

            position = request.query_params.get('position', default_position)

            if not element_serializer.is_valid():
                return Response(data={'detail': 'Inavlid element input'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                with transaction.atomic():
                    new_element = Element(**element_serializer.data, form=form)
                    new_element.save()

                    form.elements.insert(int(position), new_element.id)
                    form.save()

                    serializer = ElementSerializer(instance=new_element)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
            except DatabaseError:
                return Response(data={'detail': 'Database error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)


class ElementDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, form_id, pk):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)
            try:
                element = Element.objects.get(form=form, id=pk)
                element_serializer = ElementSerializer(element)
                return Response(data=element_serializer.data, status=status.HTTP_200_OK)
            except Element.DoesNotExist:
                return Response(data={'detail': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, form_id, pk):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)
            try:
                element = Element.objects.get(form=form, id=pk)
                element_serializer = ElementSerializer(data=request.data)

                if not element_serializer.is_valid():
                    return Response(data={'detail': 'Invalid input details', 'errors': element_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                element_serializer.update(instance=element, validated_data=element_serializer.data)

                return Response(data=element_serializer.data, status=status.HTTP_200_OK)
            except Element.DoesNotExist:
                return Response(data={'detail': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, form_id, pk):
        try:
            form = Form.objects.get(pk=form_id, user=request.user)
            print(form.elements)
            try:
                element = Element.objects.get(form=form, id=pk)
                try:
                    form.elements.remove(element.id)
                    # Performing two queries inside a transaction
                    with transaction.atomic():
                        form.save()
                        element.delete()    
                    return Response(data={'detail': 'Element deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                except DatabaseError:
                    return Response(data={'detail': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Element.DoesNotExist:
                return Response(data={'detail': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)
