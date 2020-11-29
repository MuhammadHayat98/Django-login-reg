from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
from django.template.defaultfilters import slugify
# Create your views here.
from .models import *
from .forms import CreateUserForm, newPostForm

@login_required(login_url='login')
def postNewBlog(request):
    return redirect('home')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '  + user)
                
                return redirect('login')
        context = {'form':form}
        print(request.method)
        return render(request, 'accounts/Registration.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
	    if request.method == 'POST':
		    username = request.POST.get('username')
		    password = request.POST.get('password')

		    user = authenticate(request, username=username, password=password)

		    if user is not None:
			    login(request, user)
			    return redirect('home')
		    else:
			    messages.info(request, 'Username OR password is incorrect')

	    context = {}
	    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def home(request):
    context = {
        'blogs' : Blog.objects.all().order_by('-date_posted')
    }
    return render(request, 'accounts/blog.html', context)

class BlogListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Blog
    template_name = 'accounts/blog.html'
    context_object_name = 'blogs'
    ordering = ['-date_posted']

class BlogDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Blog

class BlogCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Blog
    fields = ['subject', 'description', 'tags']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.subject)
        newpost.save()
        form.save_m2m()
        return super().form_valid(form)
    
