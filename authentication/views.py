from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from validate_email import validate_email

# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, 'Your password must be longer thar 8 characters')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'You created new account successfully!')
                return render(request, 'authentication/register.html')

        messages.danger(request, 'Username or password are already being used')
        return render(request, 'authentication/register.html', context)


class UsernameValidationView(View):
    def post(self, request):
        username = request.POST.get('username')

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'All characters in username must be alphanumeric'}, status=400)
        elif User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'This username is already taken'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        email = request.POST.get('email')

        if not validate_email(email):
            return JsonResponse({'email_error': 'Not valid email'}, status=400)
        elif User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'This email is already taken'}, status=409)
        return JsonResponse({'username_valid': True})
