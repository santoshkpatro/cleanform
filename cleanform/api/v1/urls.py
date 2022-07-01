from django.urls import path
from .auth.views import login_view, ProfileView, registration_email, RegisterView, user_status
from .forms.views import FormListView, FormDetailView
from .elements.views import ElementListCreateView, ElementDetailView


urlpatterns = [
    path('auth/status/', user_status),
    path('auth/login/', login_view),
    path('auth/register/', RegisterView.as_view()),
    path('auth/register/email/', registration_email),         # GET- ?email=ado@gmail.com&resend=True
    path('auth/profile/', ProfileView.as_view()),

    path('forms/', FormListView.as_view()),                   # POST, GET
    path('forms/<uuid:pk>/', FormDetailView.as_view()),       # GET, PUT, PATCH, DELETE
    path('forms/<uuid:form_id>/elements/', ElementListCreateView.as_view()),
    path('forms/<uuid:form_id>/elements/<str:pk>/', ElementDetailView.as_view()),
]
