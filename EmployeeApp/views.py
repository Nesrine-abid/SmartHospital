from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from EmployeeApp.models import Department, Patient, Employee, Consultation
from EmployeeApp.serializers import DepartmentSerializer, PatientSerializer, EmployeeSerializer, ConsultationSerializer
from rest_framework import status


@csrf_exempt
def patientApi(request, id=0):
    if request.method == 'GET':
        patients = Patient.objects.all()
        patients_serializer = PatientSerializer(patients, many=True)  # convert it into json format
        return JsonResponse(patients_serializer.data, safe=False)
    elif request.method == 'POST':
        patient_data = JSONParser().parse(request)
        patients_serializer = PatientSerializer(data=patient_data)  # convert it into model
        if patients_serializer.is_valid():
            patients_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        patient_data = JSONParser().parse(request)
        patient = Patient.objects.get(patientId=patient_data['patientId'])
        patients_serializer = PatientSerializer(patient, data=patient_data)
        if patients_serializer.is_valid():
            patients_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", patients_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient = Patient.objects.get(patientId=id)
        patient.info_patient.address.delete()
        patient.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def employeeApi(request, id=0):
    if request.method == 'GET':
        employees = Employee.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(employees_serializer.data, safe=False)
    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        employees_serializer = EmployeeSerializer(data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        employee_data = JSONParser().parse(request)
        employee = Employee.objects.get(employeeId=employee_data['employeeId'])
        employees_serializer = EmployeeSerializer(employee, data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        employee = Employee.objects.get(employeeId=id)
        employee.info_Employee.address.delete()
        employee.delete()
        return JsonResponse("Deleted Successfully", safe=False)



def consultationToDictionary(consultation):
    data = {}
    data['consultationId'] = consultation.consultationId
    data['doctor'] = consultation.doctor.employeeId
    data['patient'] = consultation.patient.patientId
    data['appointmentDate'] = consultation.appointmentDate
    data['appointmentState'] = consultation.appointmentState
    data['prescriptionImage'] = consultation.prescriptionImage
    data['prescriptionText'] = consultation.prescriptionText
    data['doctorNotes'] = consultation.doctorNotes
    data['temperature'] = consultation.temperature
    data['bloodPressure'] = consultation.bloodPressure

    return data


class CustomEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImageFieldFile):
            return obj.name
        return super(CustomEncoder, self).default(obj)

@csrf_exempt
def consultationApi(request, id=0):
    if request.method == 'GET':
        consultations = Consultation.objects.all()
        tempConsultations = []
        for i in range(len(consultations)):
            print(consultations[i])
            tempConsultations.append(
                consultationToDictionary(consultations[i]))  # Converting `QuerySet` to a Python Dictionary
        consultations = tempConsultations
        return JsonResponse(consultations, encoder=CustomEncoder, safe=False)
    elif request.method == 'POST':
        consultation_data = JSONParser().parse(request)
        consultation_serializer = ConsultationSerializer(data=consultation_data)
        if consultation_serializer.is_valid():
            consultation_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        consultation_data = JSONParser().parse(request)
        consultation = Consultation.objects.get(consultationId=consultation_data['consultationId'])
        # print("consultation_data",consultationToDictionary(consultation_data))
        # print("consultation",consultationToDictionary(consultation))
        consultation_serializer = ConsultationSerializer(consultationToDictionary(consultation), data=consultation_data)
        if consultation_serializer.is_valid():
            consultation_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        consultation = Consultation.objects.get(consultationId=id)
        consultation.delete()
        return JsonResponse("Deleted Successfully", safe=False)


# @csrf_exempt
# def SaveFile(request):
#     file = request.FILES['file']
#     file_name = default_storage.save(file.name, file)
#     return JsonResponse(file_name, safe=False)


@csrf_exempt
def defaultApi(request):
    return HttpResponse("hello I am working")
