from django.urls import path
from .views import RegisterView, UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'), 
    path("username-validation/", csrf_exempt(UsernameValidationView.as_view()), name='username-validation'), 
    path("email-validation/", csrf_exempt(EmailValidationView.as_view()), name='email-validation'), 

]