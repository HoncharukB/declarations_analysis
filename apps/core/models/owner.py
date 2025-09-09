from django.db import models


class OwnerType(models.TextChoices):
    DECLARANT = 'declarant', 'Декларант'
    FAMILY = 'family', 'Член сім’ї'
    PERSON = 'person', 'Фізична особа (третя)'
    COMPANY = 'company', 'Юридична особа/компанія'
    STATE = 'state', 'Держава'
    OTHER = 'other', 'Інше'

class Owner(models.Model):
    # Звичайні поля
    owner_type = models.CharField(max_length=50, choices=OwnerType.choices)
    name = models.CharField(max_length=500, null=True, blank=True)
    identifier = models.CharField(max_length=150, null=True, blank=True)
    # Зв'язки
    declarant = models.ForeignKey("Declarant", on_delete=models.SET_NULL, null=True, blank=True)
    family_member = models.ForeignKey("FamilyMember", on_delete=models.SET_NULL, null=True, blank=True)
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.owner_type == OwnerType.DECLARANT and self.declarant:
            return f"Декларант: {self.declarant}"
        elif self.owner_type == OwnerType.FAMILY and self.family_member:
            return f"Член сім’ї: {self.family_member}"
        elif self.owner_type == OwnerType.COMPANY:
            return f"Компанія: {self.name}"
        elif self.owner_type == OwnerType.PERSON:
            return f"Фізична особа: {self.name or 'Невідомо'}"
        elif self.owner_type == OwnerType.STATE:
            return f"Держава: {self.name or 'Україна'}"
        return self.name or "Невідомий власник"