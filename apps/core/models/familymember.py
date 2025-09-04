from django.db import models

class FamilyMember(models.Model):
    api_id = models.CharField(max_length=50)
    declaration_id = models.CharField(max_length=50)
    relation_type = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.relation_type}: {self.surname} {self.name}"