from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, \
    api_update_patient_view, PatientListView, PatientRetrieveUpdateDestroyView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/login', LoginView.as_view(), name='register'),
    path('accounts/logout', LogoutView.as_view(), name='register'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='register'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('patient', PatientListView.as_view()),
    path('patient/<int:pk>', PatientRetrieveUpdateDestroyView.as_view()),
    # path('patient/update/<int:pk>', PatientUpdateView.as_view()),
]
