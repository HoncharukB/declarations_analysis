from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    photo = models.ImageField(upload_to='user_photos', null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)

    declarant = models.ManyToManyField("core.Declarant", through="UserDeclarant", related_name='customer_users')
    declarations = models.ManyToManyField("core.Declaration",through="UserDeclaration",related_name='customer_users')


class UserDeclaration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    declaration = models.ForeignKey("core.Declaration", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']


class UserDeclarant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    declarant = models.ForeignKey("core.Declarant", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']
