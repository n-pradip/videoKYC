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


class OTPVerificationViewSet(viewsets.ModelViewSet):
    queryset = OTPVerification.objects.all()
    serializer_class = OTPVerificationSerializer

    # @action()
    def generate_otp():
        import random