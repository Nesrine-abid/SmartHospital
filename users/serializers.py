from rest_framework import serializers
from .models import User, Information, Address


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'cin', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(email=self.validated_data['email'], cin=self.validated_data['cin'])
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
        model = User
        fields = (
        'patientId', 'occupation', 'chronic_disease', 'allergy', 'info_patient', 'consultations', 'staff_medical')

    def create(self, validated_data):
        info_data = validated_data.pop('info_patient')
        info = InformationSerializer.create(InformationSerializer(), validated_data=info_data)
        patient, created = User.objects.update_or_create(info_patient=info,
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
