from abc import ABC

from rest_framework import serializers
from rest_framework.parsers import FileUploadParser

from .models import Information, Address, File, Patient, User


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('fileId', 'file')


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)


    class Meta:
        model = Patient
        fields = ['email', 'cin', 'password', 'password2', 'firstName',
                  'lastName', 'phone', 'passport', 'nationality', 'date_of_Birth',
                  'gender']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        patient = Patient(email=self.validated_data['email'], cin=self.validated_data['cin'],
                          firstName=self.validated_data['firstName']
                          , lastName=self.validated_data['lastName'], phone=self.validated_data['phone'],
                          passport=self.validated_data['passport'], nationality=self.validated_data['nationality'],
                          gender=self.validated_data['gender'],date_of_Birth=self.validated_data['date_of_Birth'],
                    )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        patient.set_password(password)
        patient.is_Patient = True
        patient.save()
        return patient

class RegistrationSerializerWeb(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Patient
        fields = ['email','cin', 'password', 'password2', 'firstName',
                  'lastName', 'phone', 'passport', 'nationality', 'date_of_Birth',
                  'gender','occupation', 'chronic_disease', 'allergy']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        patient = Patient(email=self.validated_data['email'], cin=self.validated_data['cin'],
                          firstName=self.validated_data['firstName']
                          , lastName=self.validated_data['lastName'], phone=self.validated_data['phone'],
                          passport=self.validated_data['passport'], nationality=self.validated_data['nationality'],
                          gender=self.validated_data['gender'],date_of_Birth=self.validated_data['date_of_Birth'],
                          occupation=self.validated_data['occupation'],chronic_disease=self.validated_data['chronic_disease'],
                          allergy=self.validated_data['allergy']
                          )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        patient.set_password(password)
        patient.is_Patient = True
        patient.save()
        return patient


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


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


class InformationSerializer(serializers.ModelSerializer):
    file_ptr = FileSerializer(required=True)

    class Meta:
        model = Information
        fields = (
            'informationId','firstName', 'email', 'lastName', 'password', 'phone', 'cin', 'passport', 'nationality', 'date_of_Birth',
            'gender', 'street','country','postalCode','city', 'file_ptr')


class InformationSerializerForUpdate(serializers.ModelSerializer):
    parser_class = (FileUploadParser,)
    address_ptr = AddressSerializer(required=True)

    class Meta:
        model = Information
        fields = (
            'firstName', 'lastName', 'password', 'phone', 'cin', 'passport', 'nationality', 'date_of_Birth',
            'gender', 'address_ptr')

    def updateInfo(self, instance, validated_data):
        address_ptr = validated_data.pop('address_ptr')
        address_serializer = AddressSerializer()
        super(self.__class__, self).update(instance, validated_data)
        super(AddressSerializer, address_serializer).update(instance.address_ptr, address_ptr)

        return instance

class PatientSerializerForUpdate(serializers.ModelSerializer):


    class Meta:
        model = Patient
        fields = ('firstName',
                  'lastName', 'phone','nationality', 'date_of_Birth',
                  'gender','chronic_disease','city','postalCode',
                  'country','street','allergy','occupation')
class PatientSerializerForGetAll(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ('user_ptr_id','firstName',
                  'lastName', 'phone','nationality', 'date_of_Birth',
                  'gender','chronic_disease','city','postalCode',
                  'country','street','allergy','occupation','file','staff_medical','date_of_Birth')

class PatientSerializer(serializers.ModelSerializer):
    information_ptr = InformationSerializer(required=False)

    class Meta:
        model = Patient
        fields = ('user_ptr_id','information_ptr',
                  'occupation', 'chronic_disease', 'allergy', 'consultations', 'staff_medical', 'is_Completed')

class PatientSerializerForConsultation(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ('user_ptr_id','firstName','lastName','cin','consultations')




# class PatientSerializerForUpdate(serializers.ModelSerializer):
#     information_ptr = InformationSerializerForUpdate(required=False)
#
#     class Meta:
#         model = Patient
#         fields = ('user_ptr_id','information_ptr',
#                   'occupation', 'chronic_disease', 'allergy')
#
#     def update(self, instance, validated_data):
#         information_ptr = validated_data.pop('information_ptr')
#         info_serializer = InformationSerializerForUpdate()
#         super(self.__class__, self).update(instance, validated_data)
#         info_serializer.updateInfo(instance.information_ptr, information_ptr)
#         return instance
