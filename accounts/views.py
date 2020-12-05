from django.shortcuts import render, redirect 
from django.http import HttpResponse
from datetime import date,datetime
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
from django.db.models import Count
from django.db.models.aggregates import Max
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
    # uX = User.objects.filter(username=request.GET.get('X')).get()
    # uY = User.objects.filter(username=request.GET.get('Y')).get()
    # if request.method == "GET":
    #     t = (Profile.objects.filter(user=uX).get().following.all() | Profile.objects.filter(user=uY).get().following.all()).distinct()
    #     print(t)
    if 'X' and 'Y' in request.GET:
        uX = User.objects.filter(username=request.GET.get('X')).get()
        uY = User.objects.filter(username=request.GET.get('Y')).get()
        t = (Profile.objects.filter(user=uX).get().following.all() & Profile.objects.filter(user=uY).get().following.all()).distinct()
        print(t)
    else:
        t = []
    context = {
        # 'blogs' : (Profile.objects.filter(user=one).get().following.all() | Profile.objects.filter(user=two).get().following.all()).distinct()
        'users' : t
    }
    return render(request, 'accounts/followsWho.html', context)

def onDate(request):
    # val = Blog.objects.filter(date_posted__date__year = '2020',date_posted__date__month = '12',date_posted__date__day = '04').count("author")
    context = {
        'users' : User.objects.raw('''
        Select id, author_id,slug,count(author_id),date_posted
            from (
            SELECT author_id,slug, COUNT(author_id),date_posted
            FROM accounts_blog  GROUP BY author_id 
            HAVING COUNT (author_id)=( 
            SELECT MAX(mycount) 
            FROM ( 
            SELECT author_id,  COUNT(author_id) mycount 
            FROM accounts_blog 
            GROUP BY author_id) )

        )where date_posted like '%2020-12-04%'
        ''')
    }
    print(context)
    return render(request, 'accounts/onDate.html', context)

def neverPosted(request):
    context = {
        'users' : User.objects.filter(blog=None)
    }
    return render(request, 'accounts/neverPosted.html', context)

def someNegative(request):
    
    context = {
        'users' : User.objects.filter(comment__pos_neg="Negative").exclude(comment__pos_neg="Positive")
    }
    return render(request, 'accounts/someNegative.html', context)

def noNegativeComments(request):
    context = {
        'users' : User.objects.exclude(blog__comment__pos_neg="Negative").exclude(blog__author__isnull=True)
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
        numComPerDay = Comment.objects.filter(author=self.request.user, date_posted__date=timezone.now().date()).count()
        numComPerPost = Comment.objects.filter(blog=self.object).count()
        if numComPerDay < 3 and numComPerPost < 1:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return redirect('home')

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
    

    def form_valid(self, form):
        numPosts = Blog.objects.filter(author=self.request.user, date_posted__date=timezone.now().date()).count()
        print(numPosts)
        if numPosts > 2:
            return redirect('home')
        else:
            form.instance.author = self.request.user
            newpost = form.save(commit=False)
            newpost.slug = slugify(newpost.subject)
            newpost.save()
            form.save_m2m()
            return super().form_valid(form)
    
    