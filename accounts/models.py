from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from django.urls import reverse
# Create your models here.

class Blog(models.Model):
    subject = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return self.subject
    
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"pk": self.pk})
    

class Comment(models.Model):
    pos_neg = models.CharField(max_length=100)
    desc = models.TextField(null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.desc



