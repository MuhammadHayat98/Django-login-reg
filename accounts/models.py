from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

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
    POS = 'Positive'
    NEG = 'Negative'
    CHOICES = [(POS, '👍'), (NEG, '👎')]
    pos_neg = models.CharField(max_length=100, choices=CHOICES, default=POS)
    desc = models.TextField(null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.desc

    def get_absolute_url(self):
        return reverse("home")

