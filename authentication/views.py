from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth
from .utils import token_generator

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
                # user.is_active = False
                user.save()
                # email_subject = 'Activate your account'

                # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # domain = get_current_site(request).domain
                # link = reverse('activate', kwargs={'uidb64': uidb64, "token": token_generator.make_token(user)})
                # activate_link = 'http://'+domain+link

                # email_body = 'hello '+user.username+' please use this link to verify your email: /n'+activate_link
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@semycolon.com',
                #     [email],
                # )
                # email.send(fail_silently=False)
                messages.success(request, 'You created new account successfully!')
                # return render(request, 'authentication/register.html')
                return redirect('login')

        messages.error(request, 'Username or password are already being used')
        return render(request, 'authentication/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            pk = force_text(urlsafe_base64_encode(uidb64))
            user = User.objects.get(pk = pk)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account successfully activated')
            return redirect('login')

        except Exception as e: 
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {user.username}')
                    return redirect('expenses')
                messages.error(request, 'Your account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Your credentials are wrong')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Fill both username and password')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been successfully logged out')
        return redirect('login')


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
