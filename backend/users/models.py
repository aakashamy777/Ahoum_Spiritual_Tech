from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('creator', 'Creator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    avatar = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
