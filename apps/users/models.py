from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
#User
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    photo = models.ImageField(upload_to='user_photos', null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)

    declarant = models.ManyToManyField("core.Declarant", related_name='customer_users')
    declarations = models.ManyToManyField("core.Declaration", related_name='customer_users')