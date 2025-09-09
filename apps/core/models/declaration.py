from django.db import models


class DeclarationType(models.IntegerChoices):
    ANNUAL = 1, "Щорічна"
    BEFORE_DISMISSAL = 2, "Перед звільненням"
    AFTER_DISMISSAL = 3, "Після звільнення"
    CANDIDATE = 4, "Кандидата на посаду"

class Declaration(models.Model):
    # Id
    document_id = models.UUIDField()
    # Звичайні поля
    declaration_year = models.PositiveSmallIntegerField()
    declaration_type = models.PositiveSmallIntegerField(choices=DeclarationType.choices)
    date = models.DateField()
    # Зв'язки
    declarant = models.ForeignKey("Declarant", on_delete=models.CASCADE, related_name='declarations')
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        type_display = dict(self._meta.get_field("declaration_type").choices).get(self.declaration_type)
        return f"Declaration {self.declaration_year} ({type_display})"