from django.urls import path
from .views import (
    RegisterView, 
    UsernameValidationView, 
    EmailValidationView, 
    VerificationView, 
    LoginView, 
    LogoutView, 
    ResetPasswordView,
    CompletePasswordReset)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'), 
    path("login/", LoginView.as_view(), name='login'), 
    path("logout/", LogoutView.as_view(), name='logout'), 
    path("reset-password/", ResetPasswordView.as_view(), name='reset-password'), 
    path("set-new-password/<uidb64>/<token>", CompletePasswordReset.as_view(), name='set-new-password'), 
    path("username-validation/", csrf_exempt(UsernameValidationView.as_view()), name='username-validation'), 
    path("email-validation/", csrf_exempt(EmailValidationView.as_view()), name='email-validation'), 
    path("activate/<uidb64>/<token>", VerificationView.as_view(), name='activate'), 
]