from django.db import models

class Declarant(models.Model):
    user_declarant_id = models.PositiveIntegerField(unique=True) #повертається ціле додатнє число, тому не змінював на UUIDField
    api_id = models.UUIDField(unique=True, null=True, blank=True)
    #
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    #
    work_place = models.CharField(max_length=255, null=True, blank=True)
    work_post = models.CharField(max_length=255, null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic or ""}'