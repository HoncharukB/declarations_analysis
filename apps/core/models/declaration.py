from django.db import models


class DeclarationType(models.IntegerChoices):
    ANNUAL = 1, "Щорічна"
    BEFORE_DISMISSAL = 2, "Після звільнення"
    AFTER_DISMISSAL = 3, "При звільненні"
    CANDIDATE = 4, "Кандидата на посаду"

class DocumentType(models.IntegerChoices):
    DECLARATION = 1, "Декларація"
    SIGNIFICANT_CHANGES = 2, "Повідомлення про суттєві зміни в майновому стані"
    DECLARATION_CORRECTED = 3, "Виправлена декларація"

class Declaration(models.Model):
    # Id
    document_id = models.UUIDField()
    # Звичайні поля
    document_type = models.PositiveSmallIntegerField(choices=DocumentType.choices)
    declaration_year = models.PositiveSmallIntegerField()
    declaration_type = models.PositiveSmallIntegerField(choices=DeclarationType.choices)
    declaration_period = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    # Зв'язки
    declarant = models.ForeignKey("Declarant", on_delete=models.CASCADE, related_name='declarations')
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean_confidential(self):
        # фільтрація
        pass

    def save(self, *args, **kwargs):
        if self.declaration_type == DeclarationType.AFTER_DISMISSAL and not self.declaration_period:
            raise ValueError("Для типу 'При звільненні' обов’язкове поле declaration_period.")
        if self.declaration_type != DeclarationType.AFTER_DISMISSAL:
            self.declaration_period = None
        self.clean_confidential()
        super().save(*args, **kwargs)

    def __str__(self):
        decl_type_display = dict(self._meta.get_field("declaration_type").choices).get(self.declaration_type, "не визначено")
        period_str = f"Період: {self.declaration_period}" if self.declaration_period else ""
        return (
            f"Декларація {self.declaration_year} рік ({decl_type_display})\n"
            f"{period_str}\n"
            f"Документ ID: {self.document_id}\n"
            f"{self.declarant}"
        )