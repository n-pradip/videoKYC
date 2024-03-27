from django.urls import path, include
from rest_framework import routers
from accounts.views import *

router = routers.DefaultRouter()

router.register(r'initial-registration', InitialRegistrationViewset)
router.register(r'user-profile', UserProfileViewset )


urlpatterns = [
    path('',include(router.urls)),

]