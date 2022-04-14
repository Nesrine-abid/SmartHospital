from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt    # to be able to allow other domains to access our api methods
from rest_framework.parsers import JSONParser      # to parse the incoming data into data model
from django.http.response import JsonResponse
from django.http import HttpResponse

from EmployeeApp.models import Department, Employee, Patient
from EmployeeApp.serializers import DepartmentSerializer, EmployeeSerializer, PatientSerializer

from django.core.files.storage import default_storage  # to save the file (last api)


@csrf_exempt
def patientApi(request, id=0):
    # return all the records in json format
    if request.method == 'GET':
        patients = Patient.objects.all()
        patients_serializer = PatientSerializer(patients, many=True)  # convert it into json format
        return JsonResponse(patients_serializer.data, safe=False)
    # POST: insert new records into department table
    elif request.method == 'POST':
        patient_data = JSONParser().parse(request)
        patients_serializer = PatientSerializer(data=patient_data)    # convert it into model
        # if the model is valid we save it into the database and return success message
        if patients_serializer.is_valid():
            patients_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    # used to update a given record
    elif request.method == 'PUT':
        patient_data = JSONParser().parse(request)
        patient = Patient.objects.get(PatientsId=patient_data['PatientId'])
        # capturing the existing record using department id
        patients_serializer = PatientSerializer(patient, data=patient_data)
        if patients_serializer.is_valid():
            patients_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        patient = Patient.objects.get(PatientsId=id)
        patient.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def departmentApi(request, id=0):
    # return all the records in json format
    if request.method == 'GET':
        departments = Department.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)  # convert it into jison format
        return JsonResponse(departments_serializer.data, safe=False)
    # POST: insert new records into department table
    elif request.method == 'POST':
        department_data = JSONParser().parse(request)
        departments_serializer = DepartmentSerializer(data=department_data)    # convert it into model
        # if the model is valid we save it into the database and return success message
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    # used to update a given record
    elif request.method == 'PUT':
        department_data = JSONParser().parse(request)
        department = Department.objects.get(DepartmentId=department_data['DepartmentId'])
        # capturing the existing record using department id
        departments_serializer = DepartmentSerializer(department, data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        department = Department.objects.get(DepartmentId=id)
        department.delete()
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
        employee = Employee.objects.get(EmployeeId=employee_data['EmployeeId'])
        employees_serializer = EmployeeSerializer(employee, data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        employee = Employee.objects.get(EmployeeId=id)
        employee.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def SaveFile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)


@csrf_exempt
def defaultApi(request):
    return HttpResponse("hello I am working")