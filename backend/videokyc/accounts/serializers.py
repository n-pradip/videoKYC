import re
from rest_framework import serializers
from .models import *
from .models import User, InitialRegistration

class InitialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialRegistration
        fields = ['id','first_name','middle_name','last_name','phone_no','email']

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        # fields=["initial_registration_attributes","bio","profile_picture","permanent_address","temporary_address",'birthdate','gender','fathers_name','mothers_name','grandfathers_name','spouse_name','role','user_document']
        exclude = ['last_login','is_email_verified','is_phone_verified']

class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
         # Check password strength requirements
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r'\d', password):
            raise serializers.ValidationError("Password must include at least one digit.")
        if not re.search(r'[!@#$%^&*()\-_=+{};:,<.>]', password):
            raise serializers.ValidationError("Password must include at least one special character.")


        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            return data
        else:
            raise serializers.ValidationError("Email and password are required.")
    


class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # exclude= ['password']

