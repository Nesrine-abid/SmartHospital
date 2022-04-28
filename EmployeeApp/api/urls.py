from django.urls import re_path
from EmployeeApp import views

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [

                  path('', views.getRoutes),
                  path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  # re_path(r'^patient/([0-9]+)$', views.patientApi),
                  #
                  # re_path(r'^patient$', views.patientApi),
                  # re_path(r'^patient/([0-9]+)$', views.patientApi),
                  #
                  # re_path(r'^employee$', views.employeeApi),
                  # re_path(r'^employee/([0-9]+)$', views.employeeApi),

                  re_path(r'^consultation$', views.api_consultation_view),
                re_path(r'^consultation/create$', views.api_create_consultation_view),
                  re_path(r'^consultation/([0-9]+)$', views.api_update_consultation_view),
                  re_path(r'^consultation/([0-9]+)/$', views.api_delete_consultation_view),

                      # re_path(r'^employee$', views.employeeApi),
                      # re_path(r'^employee/([0-9]+)$', views.employeeApi),
                      # re_path(r'^employee/savefile', views.SaveFile),

                  # re_path('', views.defaultApi),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
