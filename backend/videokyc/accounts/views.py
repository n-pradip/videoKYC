import random
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from utility.one_time_password import generate_otp_code
from django.conf import settings
from datetime import timedelta,datetime
from utility.email_handler import send_email

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']


class AddressViewSet(viewsets.ModelViewSet):
    queryset = AddressModel.objects.all()
    serializer_class = AddressSerializer
     
class InitialRegistrationViewSet(viewsets.ModelViewSet):
    """ Users initial user registration is done sending otp to user's email and saving otp in mongo collection """

    queryset = InitialRegistration.objects.all()
    serializer_class = InitialRegistrationSerializer
    http_method_names = ['get','post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            
            initial_registration_instance = serializer.instance
            otp_code = generate_otp_code(6)

            otp_document = {
                'initial_registration_id': initial_registration_instance.id,
                'otp_code': otp_code,
                'created_at': datetime.now()
            }
            settings.INITIAL_REGISTRATION_OTP_DB_COLLECTION.insert_one(otp_document)
            
            send_email(
                subject='OTP: MeroTech VKYC',
                html_path='send_initial_registration_otp.html',
                to_email = initial_registration_instance.email,
                context=otp_document
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            print(f"==== {instance.__dict__}")
            serializer = self.get_serializer(instance)
            print(f"==== {serializer}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InitialRegistration.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        queryset =   self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='verify-otp')
    def otp_verify(self, request, *args, **kwargs):
        user_provided_otp_code = request.data.get('otp_code')
        initial_registration_user_id = request.data.get('initial_registration_id')
        mongo_otp_code_obj = settings.MONGO_DB.initial_registration_otp.find({"initial_registration_id":initial_registration_user_id})

        for document in mongo_otp_code_obj:
            generated_otp_code = document["otp_code"]

        if not initial_registration_user_id or not user_provided_otp_code:
            return Response({"error": "User ID and OTP code are required"}, status=400)
        try:
            initial_registration_obj = InitialRegistration.objects.get(id=initial_registration_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=400)

        if generated_otp_code == user_provided_otp_code:
            initial_registration_obj.is_otp_verified = True
            initial_registration_obj.save()
            return Response({"message": "OTP verified successfully"}, )
        else:
            return Response({"error": "Invalid OTP code"}, status=400)

    
class InitialPasswordSetupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = SetPasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        initial_registration_id = request.data.get('initial_registration_id')

        try:
            initial_registration_obj = InitialRegistration.objects.get(id=initial_registration_id)
            if initial_registration_obj.is_otp_verified == True:
                user = User.objects.create_user(
                    email=initial_registration_obj.email,
                    password=serializer.validated_data.get('password'),
                )
                return Response({'user_id': user.id,"message": "user created sucessfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message":"User has not verified the OTP"})
        
        except InitialRegistration.DoesNotExist:
            return Response({'error': 'Initial registration data not found.'}, status=status.HTTP_404_NOT_FOUND)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        


    


    