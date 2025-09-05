from django.db import models

class FamilyMember(models.Model):
    api_id = models.UUIDField()
    declaration_id = models.UUIDField()
    #
    relation_type = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.relation_type}: {self.surname} {self.name}"