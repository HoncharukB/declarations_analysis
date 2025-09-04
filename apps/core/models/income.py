from django.db import models

class Income(models.Model):
    declaration_id = models.CharField(max_length=50)
    owner_api_id = models.UUIDField()
    object_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.object_type}: {self.amount}"