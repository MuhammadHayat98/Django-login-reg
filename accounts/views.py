from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import *
from .forms import CreateUserForm

def registerPage(request):
    form = CreateUserForm()

    return render(request, 'accounts/Registration.html')

def loginPage(request):
    return render(request, 'accounts/Login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def home(request):
    return HttpResponse('home')