from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import registerform
from django.contrib.auth import authenticate, login

def register_user(request):
    forms = registerform()
    if request.method == 'POST':
        forms = registerform(request.POST)
        if forms.is_valid():
            user = forms.save()
            username = forms.cleaned_data.get('username')
            password = forms.cleaned_data.get('password1')  # use password1 from UserCreationForm
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return render(request, 'register.html', {'forms': forms})



def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # ✅ Redirect to home route
    return render(request, 'login.html', {'form': form})



def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_user')  # Redirect to login page after logout
