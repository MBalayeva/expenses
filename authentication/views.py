from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth
from django.core.mail import EmailMessage
from .utils import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


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
                user.is_active = False
                user.save()
                email_subject = 'Activate your account'

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, "token": account_activation_token.make_token(user)})
                activate_link = 'http://'+domain+link

                email_body = 'hello '+user.username+' please use this link to verify your email: '+activate_link
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()

                messages.success(request, 'You created new account successfully, please verify it to actually be able to login!')
                return redirect('login')

        messages.error(request, 'Username or password are already being used')
        return render(request, 'authentication/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            pk = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = pk)

            if not account_activation_token.check_token(user, token):
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


        context = {
            'fieldValues': request.POST
        }

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {user.username}')
                    return redirect('expenses')
                messages.error(request, 'Your account is not active, please check your email')
                return render(request, 'authentication/login.html', context)
            messages.error(request, 'Your credentials are wrong')
            return render(request, 'authentication/login.html', context)
        
        messages.error(request, 'Fill both username and password')
        return render(request, 'authentication/login.html', context)


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



class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error('Please supply a valid email')
            return render(request, 'authentication/reset_password.html', context)

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': account_activation_token.make_token(user[0]),
            }

            link = reverse('set-new-password', kwargs={
                            'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Password reset instructions'

            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+user[0].username + ', Please click the link below to reset your password \n'+reset_url,
                'noreply@semycolon.com',
                to=[email],
            )
            EmailThread(email).start()

            messages.success(request, 'We have sent you an email to reset password')
            return render(request, 'authentication/reset_password.html', context)

        messages.error(request, 'No user with such email')
        return render(request, 'authentication/reset_password.html', context)


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:    
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)

            if not account_activation_token.check_token(user, token):
                messages.info(request, 'Link is invalid, please request a new one!')
                return redirect('login')            

        except Exception as identifier:
            pass

        return render(request, 'authentication/set_new_password.html', context)
        
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords should match')
            return render(request, 'authentication/set_new_password.html', context)

        if len(password) < 8:
            messages.error(request, 'Password should be at least 8 characters long')
            return render(request, 'authentication/set_new_password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password changed successfully!')
            return redirect('login')

        except Exception as identifier:
            messages.info(request, 'Something went wrong, please try again')
            return render(request, 'authentication/set_new_password.html', context)
