from django.db import models


class Owner(models.Model):
    OWNER_TYPE_CHOICES = [
        ('declarant', 'Декларант'),
        ('family', 'Член сім’ї'),
        ('person', 'Фізична особа (третя)'),
        ('company', 'Юридична особа/компанія'),
        ('state', 'Держава'),
        ('other', 'Інше'),
    ]

    owner_type = models.CharField(max_length=50, choices=OWNER_TYPE_CHOICES)
    #
    declarant = models.ForeignKey("Declarant", null=True, blank=True, on_delete=models.SET_NULL)
    #
    family_member = models.ForeignKey("FamilyMember", null=True, blank=True, on_delete=models.SET_NULL)
    #
    name = models.CharField(max_length=500, null=True, blank=True)
    identifier = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        if self.owner_type == "declarant" and self.declarant:
            return f"Декларант: {self.declarant}"
        elif self.owner_type == "family" and self.family_member:
            return f"Член сім’ї: {self.family_member}"
        elif self.owner_type == "company":
            return f"Компанія: {self.name}"
        elif self.owner_type == "person":
            return f"Фізична особа: {self.name or 'Невідомо'}"
        elif self.owner_type == "state":
            return f"Держава: {self.name or 'Україна'}"
        return self.name or "Невідомий власник"