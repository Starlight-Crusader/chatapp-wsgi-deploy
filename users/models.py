from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    nickname = models.CharField(unique=True, max_length=50)

    USERNAME_FIELD = 'username'
