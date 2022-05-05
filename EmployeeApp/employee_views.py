from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from EmployeeApp.api.serializers import ConsultationSerializer, PatientSerializer, EmployeeSerializer, \
    FileSerializer, DepartmentSerializer, EmployeeSerializerForUpdate
from EmployeeApp.models import Consultation, Patient, Employee, Information, Department, File


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custm claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

####################################patient#############################################
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def patientApi(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        patients_serializer = PatientSerializer(patients, many=True)  # convert it into json format
        return Response(patients_serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_patient_view(request):
    if request.method == 'POST':
        patient_serializer = PatientSerializer(data=request.data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response("Added Successfully", status=status.HTTP_201_CREATED)
        return Response("Failed to Add", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_patient_view(request,id):
    try :
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':

        operation = patient.delete()
        data = {}
        if operation :
            data["success"]="deleted successfully"
        else:
            data["failure"]="delete failed"
        return Response(data=data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_patient_view(request,id):
    try :
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        patient_serializer = PatientSerializer(patient,data=request.data)
        data = {}
        if patient_serializer.is_valid():
            patient_serializer.save()
            data["success"]="updated successfully"
            return Response(data=data)
        return Response(patient_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
############################consultation#############################################
def consultationToDictionary(consultation):
    data = {}
    data['consultationId'] = consultation.consultationId
    data['doctor'] = consultation.doctor.employeeId
    data['patient'] = consultation.patient.patientId
    data['appointmentDate'] = consultation.appointmentDate
    data['appointmentState'] = consultation.appointmentState
    # data['prescriptionImage'] = consultation.prescriptionImage
    data['prescriptionText'] = consultation.prescriptionText
    data['doctorNotes'] = consultation.doctorNotes
    data['temperature'] = consultation.temperature
    data['bloodPressure'] = consultation.bloodPressure
    return data
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def api_consultation_view(request) :
    if request.method == 'GET':
        consultations = Consultation.objects.all()
        tempConsultations = []
        for i in range(len(consultations)):
            print(consultations[i])
            tempConsultations.append(
                consultationToDictionary(consultations[i]))  # Converting `QuerySet` to a Python Dictionary
        consultations = tempConsultations
        return Response(consultations)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_consultation_view(request,id):
    try :
        consultation = Consultation.objects.get(pk=id)
    except Consultation.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        consultation_serializer = ConsultationSerializer(consultation,data=request.data)
        data = {}
        if consultation_serializer.is_valid():
            consultation_serializer.save()
            data["success"]="updated successfully"
            return Response(data=data)
        return Response(consultation_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE',])
@permission_classes([IsAuthenticated])
def api_delete_consultation_view(request,id):
    try :
        consultation = Consultation.objects.get(pk=id)
        print(consultation)
    except Consultation.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        operation = consultation.delete()
        data = {}
        if operation :
            data["success"]="deleted successfully"
        else:
            data["failure"]="delete failed"
        return Response(data=data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_consultation_view(request):
    if request.method == 'POST':
        consultation_serializer = ConsultationSerializer(data=request.data)
        if consultation_serializer.is_valid():
            consultation_serializer.save()
            return Response("Added Successfully", status=status.HTTP_201_CREATED)
        return Response("Failed to Add", status=status.HTTP_400_BAD_REQUEST)
#############################employeeeeeeeeeeeeee###################################
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def employeeApi(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)  # convert it into json format
        return Response(employees_serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_employee_view(request):
    if request.method == 'POST':
        employee_serializer = EmployeeSerializer(data=request.data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return Response("Added Successfully", status=status.HTTP_201_CREATED)
        return Response("Failed to Add", status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated, ]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializerForUpdate
#################################file_upload###############################"
class FileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated, ]
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileUploadView(generics.RetrieveUpdateDestroyAPIView):
    parser_class = (FileUploadParser,)
    permission_classes = [IsAuthenticated, ]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
      file_serializer = FileSerializer(data=request.data)
      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
######################## department####################################################
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




