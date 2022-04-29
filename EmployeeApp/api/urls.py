from django.urls import re_path
from EmployeeApp import views

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import employee_views
from .employee_views import MyTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views



from .views import RegistrationView, LogoutView, LoginView, ChangePasswordView

app_name = 'EmployeeApp'

urlpatterns = [
                path('accounts/register', RegistrationView.as_view(), name='register'),
                path('accounts/login', LoginView.as_view(), name='register'),
                path('accounts/logout', LogoutView.as_view(), name='register'),
                path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
                path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),


                  re_path(r'^patient$', employee_views.patientApi),
                  re_path(r'^patient/create$', employee_views.api_create_patient_view),
                  re_path(r'^patient/([0-9]+)$', employee_views.api_update_patient_view),
                  re_path(r'^patient/([0-9]+)/$', employee_views.api_delete_patient_view),

                  re_path(r'^employee$', employee_views.employeeApi),
                  re_path(r'^employee/create$', employee_views.api_create_employee_view),
                  re_path(r'^employee/([0-9]+)$', employee_views.api_update_employee_view),
                  re_path(r'^employee/([0-9]+)/$', employee_views.api_delete_employee_view),

                  re_path(r'^consultation$', employee_views.api_consultation_view),
                  re_path(r'^consultation/create$', employee_views.api_create_consultation_view),
                  re_path(r'^consultation/([0-9]+)$', employee_views.api_update_consultation_view),
                  re_path(r'^consultation/([0-9]+)/$', employee_views.api_delete_consultation_view),

                      # re_path(r'^employee$', views.employeeApi),
                      # re_path(r'^employee/([0-9]+)$', views.employeeApi),
                      # re_path(r'^employee/savefile', views.SaveFile),

                  # re_path('', views.defaultApi),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
