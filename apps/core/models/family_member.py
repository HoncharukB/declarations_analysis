from django.db import models


class FamilyMember(models.Model):
    # Id
    api_id = models.UUIDField()
    # Звичайні поля
    relation_type = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, null=True, blank=True)
    # Зв'язки
    declarations = models.ManyToManyField("Declaration", related_name='family_members')
    owner = models.OneToOneField("Owner", on_delete=models.CASCADE, related_name="family_member")
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.relation_type}: {self.surname} {self.name}"