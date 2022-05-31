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
from .models import *
from .emailVerification import send_otp_via_email
from .serializers import RegistrationSerializer, PasswordChangeSerializer, PatientSerializer, VerifyAccountSerializer, \
    PatientSerializerForUpdate, FileSerializer, RegistrationSerializerWeb, InformationSerializer, \
    PatientSerializerForConsultation


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

class RegistrationViewWeb(APIView):
    def post(self, request):
        serializer = RegistrationSerializerWeb(data=request.data)
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
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)  # Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'msg': 'Successfully changed'} , status=status.HTTP_204_NO_CONTENT)


# get list of all patients
class PatientListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


# delete patient by id and update patient by id (email dosent update)
class PatientUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializerForUpdate

#get file by id

class fileUpdateRetrive(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    queryset = File.objects.all()
    serializer_class = FileSerializer


# get patient by id (patient/id)
class PatientRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# get patient by id (patient/id) for consultation
class PatientRetrieveViewForConsultation(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializerForConsultation




class InformationRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


