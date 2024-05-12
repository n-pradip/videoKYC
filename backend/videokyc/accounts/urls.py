from django.urls import path, include
from rest_framework import routers
from accounts.views import *

router = routers.DefaultRouter()

router.register(r'address', AddressViewSet, basename='address')
router.register(r'initial-registration', InitialRegistrationViewSet, basename='initialregistration')
router.register(r'initial-password-setup', InitialPasswordSetupViewSet, basename='set-user-password')
router.register(r'userprofile-registration-completion', UserSignupViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'all-users', UserViewSet, basename='get_all_user')


urlpatterns = [
    path('',include(router.urls)),
    # path('', )

]