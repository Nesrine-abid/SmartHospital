from rest_framework import serializers
from EmployeeApp.models import Departments, Employees, Patients

# help to convert the complex type or model instences into native python data types
# that can be easily rendered into json or xml or other content types.
# they also help in deserialization which is nothing but converting the past data back to complex types.


class PatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ('PatientsId', 'FirstName', 'LastName', 'Email_Address', 'Telephone', 'CIN', 'Address',
                  'Gender', 'Date_of_Birth', 'Occupation', 'Chronic_disease', 'Allergy')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('DepartmentId', 'DepartmentName')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('EmployeeId', 'EmployeeName', 'Department', 'DateOfJoining', 'PhotoFileName')