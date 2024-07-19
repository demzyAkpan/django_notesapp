# from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import View
from .utility import generate_otp
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class HomePageView(View):
    template_name = 'home.html'

    def get(self, request):

        return render(request, self.template_name)
    
class UserSignup(View):

    template_name = 'signup.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
       
        if password != confirm_password:
            return redirect('accounts:signup')
        else:
            request.session['username'] = username #this place might not be needed
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('accounts:login')
        
class Login(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            return redirect('accounts:login')
        
class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:home')
    
class SendOtp(View):
    template_name = 'send_otp.html'

    def get(self, request):
        otp = generate_otp()
        request.session['otp'] = otp
        context = {
            'otp': otp
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        email_address = request.POST['email_address']
        request.session['email_address'] = email_address
        user = User.objects.get(email=email_address)

        body = f'the otp >> {request.session['otp']} and incase you forgot your username is {user.username}'
        send_mail(
            'Password reset',
            body,
            from_email='preciousakpe266@gmail.com',
            recipient_list=[email_address]
        )

        return redirect('accounts:otp_check')
    
class Check(View):
    template_name = 'check.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        otp_checker = request.POST['otp_checker']
        
        if otp_checker != request.session['otp']:
            return redirect('accounts:otp_check')
        else:
            return redirect('accounts:change_password')
        
class Password_reset(View):
    template_name = 'password_change.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user = User.objects.get(email=request.session['email_address'])
        reset = request.POST['reset']
        print(reset)
        user.set_password(reset)
        user.save()
        return redirect('accounts:login')