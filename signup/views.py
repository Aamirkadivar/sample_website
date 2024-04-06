from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import LoginForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from .models import Doctor

from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializer import UserSerializer


from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BasicAuthentication


class HomeAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'signup/password_reset.html'
    email_template_name = 'signup/password_reset_email.html'
    subject_template_name = 'signup/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  
                return redirect('home')
            else:
                messages.error(request, "•Invalid username or password!")  
    else:
        form = LoginForm()
    return render(request, 'signup/login.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


# signup page
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                nid = form.cleaned_data['national_id']
                if not user:
                    raise ValueError('Not Saved!!')
                image = request.FILES.getlist('profile_picture')
                doc = Doctor(userid = user, national_id=nid, profile_picture=image[0])
                doc.save()
                login(request, user)
                return redirect('home')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            messages.error(request,f'Sign up failed. An  error occured: {str(e)}') 
    else:
        form = SignUpForm()
        return render(request, 'signup/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.doctor)
        print("goraz1")
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print("goraz2")
            return redirect('home')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.doctor)

    return render(request, 'signup/profile.html', {'user_form': user_form, 'profile_form': profile_form})