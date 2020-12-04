from django.shortcuts import render, redirect 
from django.http import HttpResponse
from datetime import date
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from taggit.models import Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
# Create your views here.
from .models import *
from .forms import CreateUserForm, newPostForm, commentForm

@login_required(login_url='login')
def postNewBlog(request):
    return redirect('home')

# def check_user(request):

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

def positive(request):
    user = request.user
    context = {
        'blogs' : Blog.objects.filter(author=user).filter(comment__pos_neg='Positive').exclude(comment__pos_neg="Negative")
    }
    return render(request, 'accounts/positive.html', context)

def followsWho(request):
     
    # two = (User.objects.filter(user=request.Y)).get()
    # one = (User.objects.filter(user=request.X)).get()
    context = {
        # 'blogs' : (Profile.objects.filter(user=one).get().following.all() | Profile.objects.filter(user=two).get().following.all()).distinct()
        'blogs' : Blog.objects.all().order_by('-date_posted')
    }
    return render(request, 'accounts/followsWho.html', context)

def onDate(request):
    context = {
        'blogs' : Blog.objects.all().order_by('-date_posted')
    }
    return render(request, 'accounts/onDate.html', context)

def neverPosted(request):
    context = {
        'blogs' : Blog.objects.all().order_by('-date_posted')
    }
    return render(request, 'accounts/neverPosted.html', context)

def someNegative(request):
    context = {
        'blogs' : Blog.objects.all().order_by('-date_posted')
    }
    return render(request, 'accounts/someNegative.html', context)

def noNegativeComments(request):
    context = {
        'blogs' : Blog.objects.all().order_by('-date_posted')
    }
    return render(request, 'accounts/noNegativeComments.html', context)

class BlogListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Blog
    template_name = 'accounts/blog.html'
    context_object_name = 'blogs'
    ordering = ['-date_posted']

class BlogDetailView(LoginRequiredMixin, FormMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Blog
    form_class = commentForm

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['form'] = commentForm(initial={'blog': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = self.object
        print(self.object.subject)
        form.save()
        return super(BlogDetailView, self).form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context_related = Comment.objects.filter(blog=self.object)[:20]
        context['related'] = context_related
        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Blog
    # form_class = newPostForm
    fields = ['subject', 'description', 'tags']
    
    def clean(self):
        cleaned_data = super().clean()
        user = self.request.user
        numPosts = Blog.objects.filter(author=user, date_posted__date=timezone.now().date()).count()
        if numPosts > 2:
            # raise forms.ValidationError("test")
            self.add_error('tags', "err")

    # def clean(self, form):
    #     numPosts = Blog.objects.filter(author=self.request.user).count()
    #     print(numPosts)
    #     if numPosts > 2:
    #         raise forms.ValidationError("Your user plan does not support more than {} posts".format(numPosts))
    #     # return super().clean(form)
    #     return self.cleaned_data
    # def get_form_kwargs(self):
    #     kwargs = {'user' : self.request.user, }
    #     return kwargs

    def form_valid(self, form):
        numPosts = Blog.objects.filter(author=self.request.user, date_posted__date=timezone.now().date()).count()
        print(numPosts)
        if numPosts > 1:
            return redirect('home')
        else:
            form.instance.author = self.request.user
            newpost = form.save(commit=False)
            newpost.slug = slugify(newpost.subject)
            newpost.save()
            form.save_m2m()
            return super().form_valid(form)
    
    