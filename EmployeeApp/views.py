from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from EmployeeApp.serializers import *
from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout

from users.views import get_tokens_for_user


class LoginEmployeeView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data,
                             'is_Patient': user.is_Patient,
                             'is_Employee': user.is_Employee,
                             'is_admin': user.is_admin,
                             }, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationEmployeeView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_create_department_view(request):
    if request.method == 'POST':
        department_serializer = DepartmentSerializer(data=request.data)
        if department_serializer.is_valid():
            department_serializer.save()
            return Response("Added Successfully", status=status.HTTP_201_CREATED)
        return Response("Failed to Add", status=status.HTTP_400_BAD_REQUEST)


class DepartmentUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# get all departments
class DepartmentListView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated, ]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# get all employees
class EmployeeListView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerForGet


# delete employee by id and update employee by id (email dosent update)
class EmployeeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerForUpdate

# get employee by id to get file id (employee/id)
class EmployeeGetFileRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerForGetFile


# get employee by id (employee/id)
class EmployeeRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
#create consultation
class ConsultatitionRetrieveView(generics.CreateAPIView):
    # parser_class =  [MultiPartParser]
    # queryset = Consultation.objects.all()
    # serializer_class = ConsultationSerializer
    def post(self, request, *args, **kwargs):
        consultation_serializer = ConsultationSerializerForCreate(data=request.data)
        if consultation_serializer.is_valid():
            consultation_serializer.save()
            return Response(consultation_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(consultation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get consultation by id
class ConsultationRetrieveView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Consultation.objects.all().filter()
        serializer_class = ConsultationSerializerForUpdate

# get all consultations
class ConsultationListView(generics.ListCreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer





class InformationRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Information.objects.all()
    serializer_class = EmployeeSerializer
