from rest_framework import viewsets
from kyc.models import AppointmentModel, KYC
from kyc.serializers import AppointmentSerializer, KYCSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = AppointmentModel.objects.all()
    serializer_class = AppointmentSerializer

class KYCViewSet(viewsets.ModelViewSet):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer


