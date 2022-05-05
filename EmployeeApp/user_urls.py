

from django.urls import re_path ,path


from django.conf.urls.static import static
from django.conf import settings

from EmployeeApp import employee_views
from EmployeeApp.employee_views import FileUploadView, EmployeeRetrieveUpdateDestroyView

app_name = 'EmployeeApp'
urlpatterns = [


                  re_path(r'^patient$', employee_views.patientApi),
                  re_path(r'^patient/create$', employee_views.api_create_patient_view),
                  re_path(r'^patient/([0-9]+)$', employee_views.api_update_patient_view),
                  re_path(r'^patient/([0-9]+)/$', employee_views.api_delete_patient_view),

                  re_path(r'^employee$', employee_views.employeeApi),
                  # re_path(r'^employee/([0-9]+)$', employee_views.api_update_employee_view),
                  path('employee/<int:pk>', EmployeeRetrieveUpdateDestroyView.as_view()),
                  re_path(r'^employee/([0-9]+)/$', employee_views.api_delete_employee_view),



                  re_path(r'^department$', employee_views.departmentApi),
                  re_path(r'^department/create$', employee_views.api_create_department_view),
                  re_path(r'^department/([0-9]+)$', employee_views.api_update_department_view),




                  re_path(r'^consultation$', employee_views.api_consultation_view),
                  re_path(r'^consultation/create$', employee_views.api_create_consultation_view),
                  re_path(r'^consultation/([0-9]+)$', employee_views.api_update_consultation_view),
                  re_path(r'^consultation/([0-9]+)/$', employee_views.api_delete_consultation_view),

                  re_path(r'^department/create$', employee_views.api_create_department_view),

                  re_path(r'^upload', FileUploadView.as_view())


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)