# from rest_framework import serializers
# from EmployeeApp.models import  Employee, Patient, Department
# from django import forms
# from EmployeeApp.models import *
#
# # help to convert the complex type or model instences into native python data types
# # that can be easily rendered into json or xml or other content types.
# # they also help in deserialization which is nothing but converting the past data back to complex types.
#
#
from django.forms import forms


# class InfoForm(forms.ModelForm) :
#     password = forms.CharField(widget=forms.PasswordInput)
#     class Meta :
#         model = Information
#         fields = ('firstName','lastName','email','password','phone',
#                   'cin','passport','nationality','date_of_Birth',
#                   'gender')


from rest_framework import serializers

from EmployeeApp.models import Patient, Department, Information


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = ('addressId','country', 'city','street','postalCode')

#
class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ('firstName','lastName')


class PatientSerializer(serializers.ModelSerializer):
    info_patient = InformationSerializer(required=True)
    class Meta:
        model = Patient
        fields = ('patientId','occupation', 'chronic_disease', 'allergy','info_patient'
                  )

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
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


# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = (

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('departmentId', 'departmentName')
#
#'EmployeeId', 'infoEmployee', 'Role', 'speciality', 'department', 'dateOfJoining')