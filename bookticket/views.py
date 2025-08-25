from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer
from .models import OTP
from .utils import create_and_send_otp

def tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            create_and_send_otp(user, "register")
            return Response({"detail": "Registered. OTP sent to email."}, status=201)
        return Response(serializer.errors, status=400)

class VerifyRegisterOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email"}, status=404)

        otp = OTP.objects.filter(user=user, purpose="register", code=code, is_used=False).last()
        if not otp or otp.expires_at < timezone.now():
            return Response({"detail": "Invalid or expired code"}, status=400)

        otp.is_used = True
        otp.save()
        return Response({"detail": "Registration verified. You can now login."})

class LoginStartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=400)

        if not authenticate(username=user.username, password=password):
            return Response({"detail": "Invalid credentials"}, status=400)

        create_and_send_otp(user, "login")
        return Response({"detail": "OTP sent to email."})

class LoginVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid email"}, status=404)

        otp = OTP.objects.filter(user=user, purpose="login", code=code, is_used=False).last()
        if not otp or otp.expires_at < timezone.now():
            return Response({"detail": "Invalid or expired code"}, status=400)

        otp.is_used = True
        otp.save()
        return Response({"detail": "Login success", "tokens": tokens_for_user(user)})
