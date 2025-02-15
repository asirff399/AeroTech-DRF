from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants import ROLE

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=20,null=True,blank=True,default='none',choices=ROLE)
    phone = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    