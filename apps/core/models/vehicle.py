from django.db import models
from .declaration import Declaration
from .owner import Owner


class Vehicle(models.Model):
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name='vehicles')
    owners = models.ManyToManyField(Owner, related_name='vehicles')
    #
    object_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    #
    cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    owning_date = models.DateField(null=True, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model}"