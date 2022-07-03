from rest_framework import status, generics, permissions, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from cleanform.models.submission import Submission
from cleanform.models.form import Form
from .serializers import SubmissionSerializer


class SubmissionSetPagination(pagination.LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class SubmissionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, form_id):
        try:
            form = Form.objects.get(id=form_id, user=request.user)
            submissions = Submission.objects.filter(form=form)

            paginator = SubmissionSetPagination()
            page = paginator.paginate_queryset(submissions, request)

            serializer = SubmissionSerializer(instance=page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)

            return Response(data=paginated_response.data, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Unable to find form'}, status=status.HTTP_404_NOT_FOUND)
