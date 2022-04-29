from rest_framework import serializers
from .models import User, Information, Address


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'cin', 'password', 'password2', 'occupation', 'chronic_disease', 'allergy', 'firstName',
                  'lastName', 'phone', 'passport', 'nationality', 'date_of_Birth',
                  'gender', 'country', 'city', 'street', 'postalCode','user_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(email=self.validated_data['email'], cin=self.validated_data['cin'],
                     chronic_disease=self.validated_data['chronic_disease']
                    , allergy=self.validated_data['allergy'], firstName=self.validated_data['firstName']
                    , lastName=self.validated_data['lastName'], phone=self.validated_data['phone'],
                    passport=self.validated_data['passport'], nationality=self.validated_data['nationality'],
                    date_of_Birth=self.validated_data['date_of_Birth'], gender=self.validated_data['gender'],
                    country=self.validated_data['country'], city=self.validated_data['city']
                    , street=self.validated_data['street'], postalCode=self.validated_data['postalCode'], user_image=self.validated_data['user_image'])
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
    address_ptr = AddressSerializer(required=True)

    class Meta:
        model = Information
        fields = (
            'firstName', 'lastName', 'email', 'password', 'phone', 'cin', 'passport', 'nationality', 'date_of_Birth',
            'gender', 'address_ptr', 'user_image')

    def updateInfo(self, instance, validated_data):
        address_ptr = validated_data.pop('address_ptr')
        address_serializer = AddressSerializer()
        super(self.__class__, self).update(instance, validated_data)
        super(AddressSerializer, address_serializer).update(instance.address_ptr, address_ptr)
        return


class PatientSerializer(serializers.ModelSerializer):
    information_ptr = InformationSerializer(required=False)

    class Meta:
        model = User
        fields = ('patientId', 'information_ptr',
                  'occupation', 'chronic_disease', 'allergy', 'consultations', 'staff_medical')

    def update(self, instance, validated_data):
        information_ptr = validated_data.pop('information_ptr')
        info_serializer = InformationSerializer()
        super(self.__class__, self).update(instance, validated_data)
        info_serializer.updateInfo(instance.information_ptr, information_ptr)
        return instance
