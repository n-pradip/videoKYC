from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

# Create your views here.
class CustomPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "No user found with this email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_link = f"http://yourwebsite.com/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_link}",
            "from@example.com",
            [email],
            fail_silently=False,
        )

        return Response(
            {"message": "Password reset link has been sent to your email."},
            status=status.HTTP_200_OK,
        )


class CustomPasswordChangeView(APIView):
    def post(self, request):
        uid = force_text(urlsafe_base64_decode(request.data.get("uidb64")))
        token = request.data.get("token")

        try:
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = PasswordResetTokenGenerator()

        if user is not None and token_generator.check_token(user, token):
            new_password = request.data.get("new_password")
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Password has been successfully changed."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid reset link or link has expired."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CustomLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class CustomLogoutView(APIView):
    def post(self, request):
        # Perform logout logic here
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)