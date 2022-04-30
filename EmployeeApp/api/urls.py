from django.urls import re_path
from EmployeeApp import employee_views

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from .views import RegistrationView, LogoutView, LoginView, ChangePasswordView

app_name = 'EmployeeApp'

urlpatterns = [
                path('accounts/register', RegistrationView.as_view(), name='register'),
                path('accounts/login', LoginView.as_view(), name='register'),
                path('accounts/logout', LogoutView.as_view(), name='register'),
                path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
                path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
                re_path(r'^employee/([0-9]+)$', views.api_delete_employee_view),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
