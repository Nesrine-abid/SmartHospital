from rest_framework.parsers import FileUploadParser

from EmployeeApp.models import *


from rest_framework import serializers, request


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('fileId','file')

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Employee
        fields = ['email', 'cin', 'password', 'password2', 'role', 'speciality', 'dateOfJoining','department',
                  'firstName','lastName', 'phone', 'passport', 'nationality', 'date_of_Birth',
                  'gender', 'country', 'city', 'street', 'postalCode', 'file']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = Employee(email=self.validated_data['email'], cin=self.validated_data['cin'],
                     role=self.validated_data['role']
                    ,speciality=self.validated_data['speciality'], dateOfJoining=self.validated_data['dateOfJoining'],
                    firstName=self.validated_data['firstName'], lastName=self.validated_data['lastName'], phone=self.validated_data['phone'],
                    passport=self.validated_data['passport'], nationality=self.validated_data['nationality'],department=self.validated_data['department'],
                    date_of_Birth=self.validated_data['date_of_Birth'], gender=self.validated_data['gender'],
                    country=self.validated_data['country'], city=self.validated_data['city']
                    , street=self.validated_data['street'], postalCode=self.validated_data['postalCode'],file=self.validated_data['file'])

        # self.fileString = str(file.read())
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street', 'postalCode')


class InformationSerializerForUpdate(serializers.ModelSerializer):
    parser_class = (FileUploadParser,)
    address_ptr = AddressSerializer(required=True)
    # file_ptr = FileSerializer(required=True)

    class Meta:
        model = Information
        fields = (
            'firstName', 'lastName', 'password', 'phone', 'cin', 'passport', 'nationality', 'date_of_Birth',
            'gender', 'address_ptr')
    def updateInfo(self, instance, validated_data):
        address_ptr = validated_data.pop('address_ptr')
        address_serializer = AddressSerializer()
        # file_ptr = validated_data.pop('file-ptr')
        # file_serializer = FileSerializer()
        super(self.__class__, self).update(instance, validated_data)
        super(AddressSerializer, address_serializer).update(instance.address_ptr, address_ptr)
        # super(FileSerializer, file_serializer).update(instance.file_ptr, file_ptr)
        return instance
class InformationSerializer(serializers.ModelSerializer):
    address_ptr = AddressSerializer(required=True)
    file_ptr = FileSerializer(required=True)
    class Meta:
        model = Information
        fields = (
            'firstName','email', 'lastName', 'password', 'phone', 'cin', 'passport', 'nationality', 'date_of_Birth',
            'gender', 'address_ptr','file_ptr')

    def updateInfo(self, instance, validated_data):
        address_ptr = validated_data.pop('address_ptr')
        address_serializer = AddressSerializer()
        file_ptr = validated_data.pop('file_ptr')
        file_serializer = FileSerializer()
        super(self.__class__, self).update(instance, validated_data)
        super(AddressSerializer, address_serializer).update(instance.address_ptr, address_ptr)
        super(FileSerializer, file_serializer).update(instance.file_ptr, file_ptr)
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
        fields = ('departmentId', 'departmentName','department_staff')


class EmployeeSerializer(serializers.ModelSerializer):
    information_ptr = InformationSerializer(required=False)
    department = DepartmentSerializer(required=True)

    class Meta:
        model = Employee
        fields = ('employeeId','information_ptr','role', 'speciality', 'dateOfJoining', 'department', 'patients','consultations')

    def update(self, instance, validated_data):
        information_ptr = validated_data.pop('information_ptr')
        info_serializer = InformationSerializer()
        department = validated_data.pop('department')
        department_serializer = DepartmentSerializer()
        super(self.__class__, self).update(instance, validated_data)
        info_serializer.updateInfo(instance.information_ptr, information_ptr)
        department_serializer.update(instance.department, department)
        return instance


class EmployeeSerializerForUpdate(serializers.ModelSerializer):
    information_ptr = InformationSerializerForUpdate(required=False)
    # department = DepartmentSerializer(required=True)

    class Meta:
        model = Employee
        fields = ('employeeId','information_ptr','role', 'speciality', 'dateOfJoining', 'patients','consultations')

    def update(self, instance, validated_data):
        information_ptr = validated_data.pop('information_ptr')
        info_serializer = InformationSerializerForUpdate()
        # department = validated_data.pop('department')
        # department_serializer = DepartmentSerializer()
        super(self.__class__, self).update(instance, validated_data)
        info_serializer.updateInfo(instance.information_ptr, information_ptr)
        # department_serializer.update(instance.department, department)
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
