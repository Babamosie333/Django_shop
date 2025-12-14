from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone=models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"