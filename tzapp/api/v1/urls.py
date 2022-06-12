from django.urls import path
from .auth.views import login_view, register_view, ProfileView, registration_email
from .forms.views import FormListView, FormDetailView


urlpatterns = [
    path('auth/login/', login_view),
    path('auth/register/', register_view),
    path('auth/register/email/', registration_email),         # GET- ?email=ado@gmail.com&resend=True
    path('auth/profile/', ProfileView.as_view()),

    path('forms/', FormListView.as_view()),                   # POST, GET
    path('forms/<uuid:pk>/', FormDetailView.as_view()),       # GET, PUT, PATCH, DELETE
]
