from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views
from EmployeeApp.views import RegistrationEmployeeView, EmployeeListView, EmployeeRetrieveView, \
    EmployeeUpdateDestroyView, LoginEmployeeView, api_create_department_view, departmentApi, DepartmentUpdateDelete
from users.views import  ChangePasswordView
urlpatterns = [
                  path('accounts/register/employee', RegistrationEmployeeView.as_view(), name='register'),
                  path('accounts/login/employee', LoginEmployeeView.as_view(), name='login'),
                  path('accounts/change-password/employee', ChangePasswordView.as_view(), name='change-password'),
                  path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
                  path('employees', EmployeeListView.as_view()),
                  path('employee/<int:pk>', EmployeeRetrieveView.as_view()),
                  path('employee/update/<int:pk>', EmployeeUpdateDestroyView.as_view()),
                  path('employee/delete/<int:pk>', EmployeeUpdateDestroyView.as_view()),
                  path('department/<int:pk>', DepartmentUpdateDelete.as_view()),
                  path('department/create', api_create_department_view),
                  path('departments', departmentApi),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
