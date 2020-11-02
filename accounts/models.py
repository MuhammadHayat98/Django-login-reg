from django.db import models

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
    
    