'''from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)       # делаем email уникальным
    USERNAME_FIELD = 'email'                     # логинимся по email
    REQUIRED_FIELDS = ['username']              # обязательно вводим username'''