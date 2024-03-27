from rest_framework import viewsets
from .models import *
from .serializers import *

class InitialRegistrationViewset(viewsets.ModelViewSet):
    queryset = InitialRegistration.objects.all()
    serializer_class = InitialRegistrationSerializer

class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer