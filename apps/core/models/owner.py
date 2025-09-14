from django.db import models
from apps.core.models.validators.validators import validate_owner_fields


class OwnerType(models.TextChoices):
    DECLARANT = 'declarant', 'Суб’єкт декларування'
    FAMILY = 'family', 'Член сім’ї'
    PERSON = 'person', 'Третя особа'

class CitizenType(models.TextChoices):
    UKRAINIAN_CITIZEN = "Громадянин України", "Громадянин України"
    UKRAINIAN_LEGAL_ENTITY = "Юридична особа, зареєстрована в Україні", "Юридична особа, зареєстрована в Україні"
    FOREIGN_CITIZEN = "Іноземний громадянин", "Іноземний громадянин"
    FOREIGN_LEGAL_ENTITY = "Юридична особа, зареєстрована за кордоном", "Юридична особа, зареєстрована за кордоном"

class Owner(models.Model):
    # Звичайні поля
    owner_type = models.CharField(max_length=50, choices=OwnerType.choices)
    identifier = models.CharField(max_length=150, null=True, blank=True) # id власника з API НАЗК
    citizen = models.CharField( max_length=100, choices=CitizenType.choices, null=True, blank=True)

    company_name = models.CharField(max_length=500, null=True, blank=True)
    company_code = models.CharField(max_length=50, null=True, blank=True)

    last_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)

    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        validate_owner_fields(self)

    def __str__(self):
        if self.owner_type == OwnerType.DECLARANT and hasattr(self, "declarant"):
            return f"Декларант: {self.declarant}"
        elif self.owner_type == OwnerType.FAMILY and hasattr(self, "family_member"):
            return f"Член сім’ї: {self.family_member}"
        elif self.owner_type == OwnerType.PERSON:
            full_name = " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))
            return f"Третя особа: {full_name or 'Невідомо'}"
        elif self.citizen in [CitizenType.UKRAINIAN_LEGAL_ENTITY, CitizenType.FOREIGN_LEGAL_ENTITY]:
            return f"Юридична особа: {self.company_name or 'Невідома'}"
        return self.identifier or "Невідомий власник"