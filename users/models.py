from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=255)
    nickname = models.CharField(unique=True, max_length=255)
    
    secret = models.CharField(max_length=255)
    
    online = models.BooleanField(default=False)
    contacts = models.ManyToManyField('self', symmetrical=False, blank=True)

    USERNAME_FIELD = 'username'
