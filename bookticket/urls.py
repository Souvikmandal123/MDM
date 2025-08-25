from django.urls import path
from .views import RegisterView, VerifyRegisterOTPView, LoginStartView, LoginVerifyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-register-otp/", VerifyRegisterOTPView.as_view(), name="verify_register"),
    path("login/", LoginStartView.as_view(), name="login_start"),
    path("login/verify/", LoginVerifyView.as_view(), name="login_verify"),
]
