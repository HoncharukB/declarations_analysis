from django.db import models


class Vehicle(models.Model):
    # Звичайні поля
    object_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    owning_date = models.DateField(null=True, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    # Зв'язки
    declaration = models.ManyToManyField("Declaration", related_name='vehicles')
    owners = models.ManyToManyField("Owner", related_name='vehicles')
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model}"