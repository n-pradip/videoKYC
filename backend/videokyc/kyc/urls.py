from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, KYCViewSet

router = DefaultRouter()
router.register(r'appointment', AppointmentViewSet)
router.register(r'kyc', KYCViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
