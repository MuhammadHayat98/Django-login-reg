from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class UserInfo(models.Model):
    fName = models.CharField(max_length=200, null=True)
    lName = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.fName

class MockUser(models.Model):
    firstName = models.CharField(max_length=200, null=True)
    passWord = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.firstName
    
class Blog(models.Model):
    subject = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # hashtags = models._____  should have hastags data connected
    def __str__(self):
        return self.subject

class Comment(models.Model):
    pos_neg = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    blogID = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.desc
