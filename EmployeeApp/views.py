from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from EmployeeApp.serializers import *
from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout

from users.views import get_tokens_for_user


class FileConsUpdateView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (JSONParser, MultiPartParser,)
    permission_classes = [IsAuthenticated, ]
    queryset = FileConsultation.objects.all()
    serializer_class = FileConsultationSerializer


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
                             'is_admin': user.is_admin}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationEmployeeView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'registred successfully',
                             'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_create_department_view(request):
    if request.method == 'POST':
        department_serializer = DepartmentSerializer(data=request.data)
        if department_serializer.is_valid():
            department_serializer.save()
            return Response("Added Successfully", status=status.HTTP_201_CREATED)
        return Response("Failed to Add", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def departmentApi(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)  # convert it into json format
        return Response(departments_serializer.data)


class DepartmentUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# get all employees
class EmployeeListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


# //get all doctors
class DoctorsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.filter(role="doctor")
    serializer_class = EmployeeAccountsSerializer


# get all lab staff
class LaboratoryStaffListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.filter(role="analysist")
    serializer_class = EmployeeAccountsSerializer


# get all pharmacists
class PharmacistListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.filter(role="pharmacist")
    serializer_class = EmployeeAccountsSerializer


# delete employee by id and update employee by id (email dosent update)
class EmployeeUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerForUpdate


# get employee by id (employee/id)
class EmployeeRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class createConsultation(APIView):
    def post(self, request):
        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'registred successfully',
                             'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultationListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationRetreiveSerializer


class ConsultationUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


class ConsultationUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializerForUpdate
