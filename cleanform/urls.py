from django.contrib import admin
from django.urls import path, include
from cleanform.api.views import FormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('cleanform.api.v1.urls')),

    # Public route
    path('f/<slug>/', FormView.as_view())
]
