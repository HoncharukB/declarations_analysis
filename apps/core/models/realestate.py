from django.db import models

class RealEstate(models.Model):
    declaration_id = models.UUIDField()
    owner_api_id = models.UUIDField()
    iteration = models.CharField(max_length=50, unique=True)
    #
    object_type = models.CharField(max_length=100)
    other_object_type = models.CharField(max_length=255, null=True, blank=True)
    #
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    #
    total_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_date_assessment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    owning_date = models.DateField(null=True, blank=True)
    #
    reg_number = models.CharField(max_length=100, null=True, blank=True)
    object_cost_type = models.CharField(max_length=100, null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.object_type} in {self.city}, area {self.total_area} m²"