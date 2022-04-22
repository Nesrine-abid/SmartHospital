from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from EmployeeApp.models import Department, Patient, Employee
from EmployeeApp.serializers import DepartmentSerializer, PatientSerializer, EmployeeSerializer
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


# @csrf_exempt
# def SaveFile(request):
#     file = request.FILES['file']
#     file_name = default_storage.save(file.name, file)
#     return JsonResponse(file_name, safe=False)


@csrf_exempt
def defaultApi(request):
    return HttpResponse("hello I am working")
