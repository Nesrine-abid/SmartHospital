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
        model = User
        fields = ('employeeId', 'information_ptr', 'role', 'speciality', 'dateOfJoining', 'department', 'patients',
                  'consultations')


class EmployeeSerializerForUpdate(serializers.ModelSerializer):
    information_ptr = InformationSerializerForUpdate(required=False)

    class Meta:
        model = User
        fields = ('employeeId', 'information_ptr', 'role', 'speciality', 'dateOfJoining', 'patients', 'consultations')

    def update(self, instance, validated_data):
        information_ptr = validated_data.pop('information_ptr')
        info_serializer = InformationSerializerForUpdate()
        super(self.__class__, self).update(instance, validated_data)
        info_serializer.updateInfo(instance.information_ptr, information_ptr)
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'cin', 'password', 'password2', 'firstName',
                  'lastName', 'phone', 'passport', 'nationality', 'date_of_Birth',
                  'gender']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_cleaned_data(self):
        data = {
            'role': self.validated_data.get('role', ''),
            'speciality': self.validated_data.get('speciality', ''),
            'dateOfJoining': self.validated_data.get('dateOfJoining'),
            # 'department': self.validated_data.get('department', '')
        }
        return data

    def save(self):
        user = User(email=self.validated_data['email'], cin=self.validated_data['cin'],
                    firstName=self.validated_data['firstName'], lastName=self.validated_data['lastName'],
                    phone=self.validated_data['phone'],
                    passport=self.validated_data['passport'], nationality=self.validated_data['nationality'],
                    date_of_Birth=self.validated_data['date_of_Birth'], gender=self.validated_data['gender'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.is_Employee = True
        user.save()
        employee = Employee.objects.create(user=user)
        employee.role = self.get_cleaned_data().get('role')
        employee.speciality = self.get_cleaned_data().get('speciality')
        employee.dateOfJoining = self.get_cleaned_data().get('dateOfJoining')
        print(employee.dateOfJoining)

        employee.save()
        return user


class ConsultationSerializer(serializers.ModelSerializer):
    parser_classes = [FileUploadParser]

    class Meta:
        model = Consultation
        fields = (
            'consultationId', 'appointmentDate', 'doctor', 'appointmentState', 'patient', 'appointmentState',
            'prescriptionText',
            'doctorNotes', 'temperature', 'bloodPressure')

        def update(self, instance, validated_data):
            consultations_id_pool = []

            consultations = validated_data.pop('consultations')

            consultations_with_same_profile_instance = Consultation.objects.filter(patient=instance.pk).values_list(
                'consultationId', flat=True)

            for consultation in consultations:

                if "consultationId" in consultation.keys():
                    if Consultation.objects.filter(id=consultation['consultationId']).exists():
                        consultation_instance = Consultation.objects.get(id=consultation['consultationId'])
                        consultation_instance = consultation.get('doctor', consultation_instance.doctor)
                        consultation_instance = consultation.get('patient', consultation_instance.patient)
                        consultation_instance = consultation.get('appointmentDate',
                                                                 consultation_instance.appointmentDate)
                        consultation_instance = consultation.get('prescriptionImage',
                                                                 consultation_instance.prescriptionImage)

                        consultation_instance = consultation.get('appointmentState',
                                                                 consultation_instance.appointmentState)

                        consultation_instance.prescriptionText = consultation.get('prescriptionText',
                                                                                  consultation_instance.prescriptionText)
                        consultation_instance.doctorNotes = consultation.get('doctorNotes',
                                                                             consultation_instance.doctorNotes)
                        consultation_instance.temperature = consultation.get('temperature',
                                                                             consultation_instance.temperature)
                        consultation_instance.bloodPressure = consultation.get('bloodPressure',
                                                                               consultation_instance.bloodPressure)

                        consultation_instance.save()
                        consultations_id_pool.append(consultation_instance.consultationId)

                    else:
                        continue
                else:
                    consultations = Consultation.objects.create(patient=instance, **consultation)
                    consultations_id_pool.append(consultations.consultationId)

            for consultation_id in consultations_with_same_profile_instance:
                if consultation_id not in consultations_id_pool:
                    Consultation.objects.filter(pk=consultation_id).delete()

            return instance
