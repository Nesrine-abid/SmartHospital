from rest_framework import serializers
from EmployeeApp.models import  Employee, Patient, Department
from django import forms
from EmployeeApp.models import *

# help to convert the complex type or model instences into native python data types
# that can be easily rendered into json or xml or other content types.
# they also help in deserialization which is nothing but converting the past data back to complex types.


class InfoForm(forms.ModelForm) :
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta :
        model = Information
        fields = ('firstName','lastName','email','password','phone',
                  'cin','passport','nationality','date_of_Birth',
                  'gender')


# class AddressSerializer(serializers.ModelSerializer):
#     # class Meta:
#     #     model = Address
#     #     fields = ('addressId','country', 'city','street','postalCode')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('PatientsId', 'infoPatient', 'Occupation', 'Chronic_disease', 'Allergy', 'consultations',
                  'medical_staff_Patient', 'appointmentList')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('DepartmentId', 'DepartmentName')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('EmployeeId', 'infoEmployee', 'Role', 'speciality', 'department', 'dateOfJoining')