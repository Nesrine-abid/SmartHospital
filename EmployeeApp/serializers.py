from rest_framework import serializers

from EmployeeApp.models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street', 'postalCode')


class InformationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)

    class Meta:
        model = Information
        fields = (
            'firstName', 'lastName', 'email', 'password', 'phone', 'cin', 'passport', 'nationality', 'date_of_Birth',
            'gender', 'address')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = AddressSerializer.create(AddressSerializer(), validated_data=address_data)
        info_patient, created = Information.objects.update_or_create(address=address,
                                                                     firstName=validated_data.pop('firstName'),
                                                                     lastName=validated_data.pop('lastName'),
                                                                     email=validated_data.pop('email'),
                                                                     password=validated_data.pop('password'),
                                                                     phone=validated_data.pop('phone'),
                                                                     cin=validated_data.pop('cin'),
                                                                     date_of_Birth=validated_data.pop('date_of_Birth'),
                                                                     passport=validated_data.pop('passport'),
                                                                     nationality=validated_data.pop('nationality'),
                                                                     gender=validated_data.pop('gender')

                                                                     )
        return info_patient


class PatientSerializer(serializers.ModelSerializer):
    info_patient = InformationSerializer(required=True)

    class Meta:
        model = Patient
        fields = ('patientId', 'occupation', 'chronic_disease', 'allergy', 'info_patient')

    def create(self, validated_data):
        info_data = validated_data.pop('info_patient')
        info = InformationSerializer.create(InformationSerializer(), validated_data=info_data)
        patient, created = Patient.objects.update_or_create(info_patient=info,
                                                            occupation=validated_data.pop('occupation'),
                                                            chronic_disease=validated_data.pop('chronic_disease'),
                                                            allergy=validated_data.pop('allergy')
                                                            )
        return patient

    def update(self, instance, validated_data):
        info_patient = validated_data.pop('info_patient')
        info_serializer = InformationSerializer()
        super(self.__class__, self).update(instance, validated_data)
        super(InformationSerializer, info_serializer).update(instance.info_patient, info_patient)
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('departmentId', 'departmentName')


class EmployeeSerializer(serializers.ModelSerializer):
    info_Employee = InformationSerializer(required=True)
    department = DepartmentSerializer(required=True)
    # patients = PatientSerializer(required=True)

    class Meta:
        model = Employee
        fields = ('employeeId', 'info_Employee', 'role', 'speciality', 'dateOfJoining','department')

    def create(self, validated_data):
        info_data = validated_data.pop('info_Employee')
        department = validated_data.pop('department')
        # patients = validated_data.pop('patients')
        info = InformationSerializer.create(InformationSerializer(), validated_data=info_data)
        # patients = PatientSerializer.create(PatientSerializer(), validated_data=patients)
        department = DepartmentSerializer.create(DepartmentSerializer(), validated_data=department)
        employee, created = Employee.objects.update_or_create(info_Employee=info,
                                                              # patients=patients,
                                                              department=department,
                                                              role=validated_data.pop('role'),
                                                              speciality=validated_data.pop('speciality'),
                                                              dateOfJoining=validated_data.pop('dateOfJoining')
                                                              )
        return employee
