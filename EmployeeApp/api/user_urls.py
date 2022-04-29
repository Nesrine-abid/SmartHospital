from django.urls import re_path


from django.conf.urls.static import static
from django.conf import settings

from . import employee_views
app_name = 'EmployeeApp'
urlpatterns = [


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


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)