from django.urls import path
from .views import RegistrationView, LoginView, ChangePasswordView, \
    PatientListView, VerifyOTP, PatientUpdateDestroyView, PatientRetrieveView, FileUpdateView, ConfirmAccount, \
    FileQrCodeHistoryUpdateView, FileQrCodeConsUpdateView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('accounts/register/patient', RegistrationView.as_view(), name='register'),
    path('accounts/verify', VerifyOTP.as_view(), name='verify'),
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('accounts/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('patient', PatientListView.as_view()),
    path('confirmAccount', ConfirmAccount.as_view()),
    path('patient/<int:pk>', PatientRetrieveView.as_view()),
    path('patient/update/<int:pk>', PatientUpdateDestroyView.as_view()),
    path('upload/<int:pk>', FileUpdateView.as_view()),
    path('uploadFileQrCodeHistory/<int:pk>', FileQrCodeHistoryUpdateView.as_view()),
    path('uploadFileQrCodeCons/<int:pk>', FileQrCodeConsUpdateView.as_view()),
]
