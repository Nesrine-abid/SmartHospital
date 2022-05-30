from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.parsers import FileUploadParser

from EmployeeApp.models import *
from users.serializers import InformationSerializer, InformationSerializerForUpdate


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'departmentName', 'department_staff')


class EmployeeSerializer(serializers.ModelSerializer):
    information_ptr = InformationSerializer(required=False)
    department = DepartmentSerializer(required=True)

    class Meta:
        model = Employee
        fields = ('user_ptr_id', 'information_ptr', 'role', 'speciality', 'dateOfJoining', 'department',
                  'patients',
                  'consultations')


class EmployeeAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('firstName', 'lastName', 'email', 'role', 'speciality', 'is_verified', 'user_ptr_id')


class EmployeeSerializerForUpdate(serializers.ModelSerializer):
    information_ptr = InformationSerializerForUpdate(required=False)

    class Meta:
        model = Employee
        fields = ('user_ptr_id', 'information_ptr', 'speciality', 'dateOfJoining'
                  )

    def update(self, instance, validated_data):
        information_ptr = validated_data.pop('information_ptr')
        info_serializer = InformationSerializerForUpdate()
        super(self.__class__, self).update(instance, validated_data)
        info_serializer.updateInfo(instance.information_ptr, information_ptr)
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Employee
        fields = ['email', 'cin', 'password', 'password2', 'firstName',
                  'lastName', 'phone', 'passport', 'nationality', 'date_of_Birth',
                  'gender', 'role', 'department', 'speciality', 'dateOfJoining']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        employee = Employee(email=self.validated_data['email'], cin=self.validated_data['cin'],
                            firstName=self.validated_data['firstName'], lastName=self.validated_data['lastName'],
                            phone=self.validated_data['phone'],
                            passport=self.validated_data['passport'], nationality=self.validated_data['nationality'],
                            date_of_Birth=self.validated_data['date_of_Birth'], gender=self.validated_data['gender'],
                            department=self.validated_data['department'],
                            dateOfJoining=self.validated_data['dateOfJoining'],
                            role=self.validated_data['role'], speciality=self.validated_data['speciality'], )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        employee.set_password(password)
        employee.is_Employee = True
        employee.save()
        return employee


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = (
            'consultationId', 'appointmentDate', 'appointmentTime', 'doctor', 'patient')

    def save(self):
        consultation = Consultation(appointmentDate=self.validated_data['appointmentDate'],
                                    appointmentTime=self.validated_data['appointmentTime'],
                                    doctor=self.validated_data['doctor'],
                                    patient=self.validated_data['patient'])
        if not consultation.doctor.patients.contains(self.validated_data['patient']):
            consultation.doctor.patients.add(self.validated_data['patient'])
        consultation.save()
        return consultation


class ConsultationSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = (
            'consultationId', 'appointmentDate', 'appointmentTime',
            'prescriptionText', 'prescriptionImage',
            'doctorNotes', 'temperature', 'bloodPressure')
