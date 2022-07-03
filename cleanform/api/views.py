from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from cleanform.models.form import Form
from cleanform.models.element import Element
from cleanform.models.submission import Submission


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
            'layouts',
            'validations'
        ]


class FormView(APIView):

    # GET /f/<slug>/
    def get(self, request, slug):
        try:
            form = Form.objects.get(slug=slug, is_live=True)
            elements = Element.objects.filter(form=form)
            serializer = ElementSerializer(instance=elements, many=True)
            data = {
                'title': form.title,
                'elements_order': form.elements,
                'elements': serializer.data
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, sattus=status.HTTP_404_NOT_FOUND)

    # POST /f/<slug>/
    def post(self, request, slug):
        try:
            form = Form.objects.get(slug=slug, is_live=True)
            Submission.objects.create(form=form, data=request.data)
            return Response(data={'detail': 'Submission submitted successfully'}, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)
