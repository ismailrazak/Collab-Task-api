from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_pictures/',null=True,blank=True)
    house = models.ForeignKey('house.House',on_delete=models.SET_NULL,related_name='members',null=True,blank=True)

