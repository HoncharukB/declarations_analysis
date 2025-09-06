from django.db import models
from .declaration import Declaration
from .owner import Owner


class Income(models.Model):
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name='incomes')
    owners = models.ManyToManyField(Owner, related_name='incomes')
    #
    object_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    #
    source = models.CharField(max_length=255, null=True, blank=True)
    sources = models.JSONField(null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.object_type}: {self.amount}"