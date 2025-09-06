from django.db import models
from .declaration import Declaration
from .owner import Owner


class BankAccount(models.Model):
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name='bank_accounts')
    owners = models.ManyToManyField(Owner, related_name='bank_accounts')
    #
    object_type = models.CharField(max_length=100)
    currency = models.CharField(max_length=10, null=True, blank=True)
    amount = models.PositiveBigIntegerField(null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.object_type} {self.amount} {self.currency}"