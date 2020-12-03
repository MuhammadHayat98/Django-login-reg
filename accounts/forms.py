from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Blog, Comment

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class newPostForm(ModelForm):
    subject = forms.CharField(widget=forms.TextInput(
        attrs={'class': "form-control",
               'placeholder': "Submission title"}),
        required=True, min_length=1, max_length=250)
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'rows': "3",
            'placeholder': "Optional text"}),
        max_length=5000,
        required=False)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.author = user
        super(newPostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Blog
        fields = ('subject', 'description', 'tags')

    def clean(self):
        numPosts = Blog.objects.filter(author=self.author).count()
        print(numPosts)
        if numPosts > 2:
            raise forms.ValidationError("Your user plan does not support more than {} posts".format(numPosts))
        return self.cleaned_data

class commentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('pos_neg', 'desc')