from django.db import models

class Declarant(models.Model):
    user_declarant_id = models.IntegerField(unique=True)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)

    work_place = models.CharField(max_length=255, null=True, blank=True)
    work_post = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return \
            f'{self.surname} {self.name} {self.patronymic}'