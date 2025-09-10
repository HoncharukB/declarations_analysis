from django.db import models


class Declarant(models.Model):
    # Id
    user_declarant_id = models.PositiveIntegerField(unique=True)
    api_id = models.UUIDField(unique=True, null=True, blank=True)
    # Звичайні поля
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    work_place = models.CharField(max_length=255, null=True, blank=True)
    work_post = models.CharField(max_length=255, null=True, blank=True)
    # Зв'язки
    owner = models.OneToOneField("Owner", on_delete=models.CASCADE, related_name="declarant")
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic or ""} \n{self.work_place} {self.work_post}'