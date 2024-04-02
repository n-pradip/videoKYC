import random
from rest_framework import viewsets
from .serializers import InitialRegistrationSerializer, UserSignupSerializer, LoginSerializer, OTPVerificationSerializer,SetPasswordSerializer, AddressSerializer, UserSerializer
from .models import User, InitialRegistration, OTPVerification, AddressModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']


class AddressViewSet(viewsets.ModelViewSet):
    queryset = AddressModel.objects.all()
    serializer_class = AddressSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)
        return Response({"message": f"Address with ID {instance_id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)
    

class InitialRegistrationViewSet(viewsets.ModelViewSet):
    queryset = InitialRegistration.objects.all()
    serializer_class = InitialRegistrationSerializer
    http_method_names = ['get','post']
    

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
            user = User.objects.create_user(
                email=initial_registration_obj.email,
                password=serializer.validated_data.get('password'),
                # first_name=initial_registration_obj.first_name,
                # middle_name=initial_registration_obj.middle_name,
                # last_name=initial_registration_obj.last_name,
                # phone_no=initial_registration_obj.phone_no
            )

            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        except InitialRegistration.DoesNotExist:
            return Response({'error': 'Initial registration data not found.'}, status=status.HTTP_404_NOT_FOUND)


class UserSignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    http_method_names = ['post']

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.data.get('user_id')  # Assuming the user ID is passed in the request data

        try:
            user = User.objects.get(id=user_id)
            serializer = self.get_serializer(user, data=request.data, partial=True)  # Partial update
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Optionally, you can generate tokens here as well if needed
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'user': serializer.data, 'tokens': tokens}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    # @action(detail=False, methods=['post'], url_path='login')
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

def generate_otp_code(num):
    # Generate each digit of the OTP separately and concatenate them
    otp_code = ''.join(str(random.randint(0, 9)) for _ in range(num))    
    return otp_code

class OTPVerificationViewSet(viewsets.ModelViewSet):
    queryset = OTPVerification.objects.all()
    serializer_class = OTPVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    @action(detail=False, methods=['post'], url_path='verify-otp')
    def otp_verify(self, request, *args, **kwargs):
        generated_otp_code = request.session.get('generated_otp_code')
        if not generated_otp_code:
            return Response({"error": "OTP not generated. Please send OTP first."}, status=400)

        user_id = request.data.get('user_id')
        user_provided_otp_code = request.data.get('otp_code')

        if not user_id or not user_provided_otp_code:
            return Response({"error": "User ID and OTP code are required"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=400)

        if generated_otp_code == user_provided_otp_code:
            user.is_otp_verified = True
            user.save()
            return Response({"message": "OTP verified successfully"})
        else:
            return Response({"error": "Invalid OTP code"}, status=400)
        


    


    