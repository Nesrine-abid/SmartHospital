from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from EmployeeApp.api.serializers import ConsultationSerializer, PatientSerializer
from EmployeeApp.models import Consultation, Patient


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


@api_view(['GET'])

def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)
# @csrf_exempt
#
# def patientApi(request, id=0):
#     if request.method == 'GET':
#         patients = Patient.objects.all()
#         patients_serializer = PatientSerializer(patients, many=True)  # convert it into json format
#         return JsonResponse(patients_serializer.data, safe=False)
#     elif request.method == 'POST':
#         patient_data = JSONParser().parse(request)
#         patients_serializer = PatientSerializer(data=patient_data)  # convert it into model
#         if patients_serializer.is_valid():
#             patients_serializer.save()
#             return JsonResponse("Added Successfully", safe=False)
#         return JsonResponse("Failed to Add", safe=False)
#     elif request.method == 'PUT':
#         patient_data = JSONParser().parse(request)
#         patient = Patient.objects.get(patientId=patient_data['patientId'])
#         patients_serializer = PatientSerializer(patient, data=patient_data)
#         if patients_serializer.is_valid():
#             patients_serializer.save()
#             return JsonResponse("Updated Successfully", safe=False)
#         return JsonResponse("Failed to Update", patients_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         patient = Patient.objects.get(patientId=id)
#         patient.info_patient.address.delete()
#         patient.delete()
#         return JsonResponse("Deleted Successfully", safe=False)


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
def patientApi(request, id=0):
    if request.method == 'GET':
        patients = Patient.objects.all()
        patients_serializer = PatientSerializer(patients, many=True)  # convert it into json format
        return Response(patients_serializer)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_consultation_view(request):
        request.method == 'POST':
        patient_data = JSONParser().parse(request)
        patients_serializer = PatientSerializer(data=patient_data)  # convert it into model
        if patients_serializer.is_valid():
            patients_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)


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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_consultation_view(request,id):
    print('sssssssssss')
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

