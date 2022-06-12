from rest_framework import generics, permissions, serializers, pagination, status
from rest_framework.views import APIView
from rest_framework.response import Response
from tzapp.models.form import Form


class FormOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class FormListPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_query_param = 'page_size'


class FormListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            'id',
            'title',
            'description',
            'is_live',
            'created_at',
        ]


class FormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            'id',
            'title',
            'description',
            'is_live',
            'order',
            'created_at',
        ]


class FormListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FormListSerializer
    queryset = Form.objects.all()
    pagination_class = FormListPagination

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FormDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, FormOwnerPermission]
    serializer_class = FormDetailSerializer
    queryset = Form.objects.all()


class FormBuilderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            form = Form.objects.get(pk=pk, user=request.user)
            return Response(data={'detail': 'Success'}, status=status.HTTP_200_OK)
        except Form.DoesNotExist:
            return Response(data={'detail': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)
