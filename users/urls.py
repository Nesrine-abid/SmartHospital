from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, \
    api_update_patient_view, PatientListView, PatientRetrieveUpdateDestroyView, VerifyOTP
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('accounts/register', RegistrationView.as_view(), name='register'),
    path('accounts/verify', VerifyOTP.as_view(), name='verify'),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('patient', PatientListView.as_view()),
    path('patient/<int:pk>', PatientRetrieveUpdateDestroyView.as_view()),
    # path('patient/update/<int:pk>', PatientUpdateView.as_view()),
]
