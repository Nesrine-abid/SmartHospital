from rest_framework import serializers
from rest_framework.parsers import FileUploadParser

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

    def updateInfo(self, instance, validated_data):
        address = validated_data.pop('address')
        address_serializer = AddressSerializer()
        super(self.__class__, self).update(instance, validated_data)
        super(AddressSerializer, address_serializer).update(instance.address, address)
        return instance


class PatientSerializer(serializers.ModelSerializer):
    info_patient = InformationSerializer(required=True)

    class Meta:
        model = Patient
        fields = ('patientId', 'occupation', 'chronic_disease', 'allergy', 'info_patient', 'consultations','staff_medical')

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
        info_serializer.updateInfo(instance.info_patient, info_patient)
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('departmentId', 'departmentName')


class EmployeeSerializer(serializers.ModelSerializer):
    info_Employee = InformationSerializer(required=True)
    department = DepartmentSerializer(required=True)

    class Meta:
        model = Employee
        fields = ('employeeId', 'info_Employee', 'role', 'speciality', 'dateOfJoining', 'department', 'patients','consultations')

    def create(self, validated_data):
        # departments = Department.objects.all()
        info_data = validated_data.pop('info_Employee')
        department = validated_data.pop('department')
        department = DepartmentSerializer.create(DepartmentSerializer(), validated_data=department)
        info = InformationSerializer.create(InformationSerializer(), validated_data=info_data)
        employee, created = Employee.objects.update_or_create(info_Employee=info,
                                                              department=department,
                                                              role=validated_data.pop('role'),
                                                              speciality=validated_data.pop('speciality'),
                                                              dateOfJoining=validated_data.pop('dateOfJoining')
                                                              )
        return employee

    def update(self, instance, validated_data):
        info_Employee = validated_data.pop('info_Employee')
        info_serializer = InformationSerializer()
        department = validated_data.pop('department')
        department_serializer = DepartmentSerializer()
        super(self.__class__, self).update(instance, validated_data)
        info_serializer.updateInfo(instance.info_Employee, info_Employee)
        department_serializer.update(instance.department, department)
        return instance


class ConsultationSerializer(serializers.ModelSerializer):
    parser_classes = [FileUploadParser]

    class Meta:
        model = Consultation
        fields = (
            'consultationId', 'appointmentDate','doctor','appointmentState','patient','appointmentState' , 'prescriptionText',
            'doctorNotes','temperature', 'bloodPressure')


        def update(self, instance, validated_data):
            consultations_id_pool = []

            consultations = validated_data.pop('consultations')

            consultations_with_same_profile_instance = Consultation.objects.filter(patient=instance.pk).values_list(
                'consultationId', flat=True)

            for consultation in consultations:

                if "consultationId" in consultation.keys():
                    if Consultation.objects.filter(id=consultation['consultationId']).exists():
                        consultation_instance = Consultation.objects.get(id=consultation['consultationId'])
                        consultation_instance = consultation.get('doctor',consultation_instance.doctor)
                        consultation_instance = consultation.get('patient', consultation_instance.patient)
                        consultation_instance = consultation.get('appointmentDate', consultation_instance.appointmentDate)
                        consultation_instance = consultation.get('prescriptionImage',consultation_instance.prescriptionImage)

                        consultation_instance = consultation.get('appointmentState', consultation_instance.appointmentState)

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




    # def update(self, instance, validated_data):
    #     doctor = validated_data.pop('doctor')
    #     patient = validated_data.pop('patient')
    #     print(patient)
    #     patient_serializer = PatientSerializer()
    #     doctor_serializer = EmployeeSerializer()
    #     super(self.__class__, self).update(instance, validated_data)
    #     patient_serializer.update(instance.patientId, patient)
    #     doctor_serializer.update(instance.employeeId, doctor)
    #     return instance
