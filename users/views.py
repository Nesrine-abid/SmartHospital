from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from EmployeeApp.models import Employee
from .models import *
from .emailVerification import send_otp_via_email
from .serializers import RegistrationSerializer, PasswordChangeSerializer, PatientSerializer, VerifyAccountSerializer, \
    PatientSerializerForUpdate, FileSerializer, ConfirmAccountSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# post a patient
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data['email'])
            send_otp_via_email(serializer.data['email'])
            return Response({'msg': 'registred successfully',
                             'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTP(APIView):
    def post(self, request):
        data = request.data
        serializer = VerifyAccountSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = Patient.objects.filter(email=email)
            if not user.exists():
                return Response({
                    'status': 400,
                    'message': 'there is no patient with this email'
                })
            if user[0].otp != otp:
                return Response({
                    'message': 'wrong otp'
                })
            user = user.first()
            user.is_verified = True
            user.save()
            return Response({
                'status': 200,
                'message': 'account verified'
            })
        return Response({
            'status': 400,
            'message': 'something went wrong',
            'data': serializer.errors
        })

    def patch(self, request):
        data = request.data
        serializer = VerifyAccountSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            user = Patient.objects.filter(email=email)
            if not user.exists():
                return Response({
                    'status': 400,
                    'message': 'there is no patient with this email'
                })
            status = send_otp_via_email(email)
            if status:
                return Response({
                    'status': 200,
                    'message': 'new otp sent'
                })

            return Response({
                'status': 400,
                'message': 'try after few seconds later , resent is after one minute'
            })
        return Response({
            'status': 400,
            'message': 'something went wrong',
            'data': serializer.errors
        })


class FileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated, ]
    queryset = File.objects.all()
    serializer_class = FileSerializer


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            print("user", user.is_Patient)
            return Response({'msg': 'Login Success', **auth_data,
                             'is_Patient': user.is_Patient,
                             'is_Employee': user.is_Employee,
                             'is_admin': user.is_admin}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated, ]
#     def post(self, request):
#         logout(request)
#         return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'msg': 'Successfully changed'}, status=status.HTTP_204_NO_CONTENT)


# get list of all patients
class PatientListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


# delete patient by id and update patient by id (email dosent update)
class PatientUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializerForUpdate


# get patient by id (patient/id)
class PatientRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_patient_view(request, id):
    try:
        patient = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        patient_serializer = PatientSerializer(patient, data=request.data)
        data = {}
        if patient_serializer.is_valid():
            patient_serializer.save()
            data["success"] = "updated successfully"
            return Response(data=data)
        return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@permission_classes([IsAuthenticated])
def patientUpdateApi(request, id=0):
    if request.method == 'PUT':
        patient_data = JSONParser().parse(request)
        patient = User.objects.get(patientId=patient_data['patientId'])
        patients_serializer = PatientSerializer(patient, data=patient_data)
        if patients_serializer.is_valid():
            patients_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", patients_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAccount(APIView):
    def post(self, request):
        data = request.data
        serializer = ConfirmAccountSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            employee = Employee.objects.filter(email=email)
            if not employee.exists():
                return Response({
                    'status': 400,
                    'message': 'there is no employee with this email'
                })
            employee = employee.first()
            employee.is_verified = True
            employee.save()
            return Response({
                'status': 200,
                'message': 'account confirmed'
            })
        return Response({
            'status': 400,
            'message': 'something went wrong',
            'data': serializer.errors
        })
