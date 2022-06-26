from django.utils.text import slugify
from rest_framework import generics, permissions, serializers, pagination, status
from rest_framework.views import APIView
from rest_framework.response import Response
from nanoid import generate
from cleanform.models.form import Form
from cleanform.models.element import Element


class FormOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class FormListPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_query_param = 'page_size'


class ElementDetailSerializer(serializers.ModelSerializer):
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
        ]


class FormListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Form
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'is_live',
            'created_at',
        ]
        extra_kwargs = {
            'slug': {
                'required': False
            }
        }

    def create(self, validated_data):
        slug = validated_data.get('slug', None)
        if not slug:
            slug = slugify(validated_data.get('title')) + "-" + generate(size=10)
        return Form.objects.create(**validated_data, slug=slug)


class FormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            'id',
            'title',
            'description',
            'is_live',
            'elements',
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
