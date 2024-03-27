from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class InitialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialRegistration
        # fields = ['first_name','middle_name','last_name','phone_no','email','created_at','updated_at']
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
