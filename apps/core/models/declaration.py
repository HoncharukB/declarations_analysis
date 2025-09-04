from django.db import models

class Declaration(models.Model):
    document_id = models.UUIDField(primary_key=True)
    user_declarant_id = models.PositiveIntegerField()
    declaration_year = models.PositiveIntegerField()
    declaration_type = models.PositiveSmallIntegerField(
        choices=[(1, "Щорічна"), (2, "Перед звільненням"), (3, "Після звільнення"), (4, "Кандидата на посаду")]
    )
    date = models.DateField()

    def __str__(self):
        type_display = dict(self._meta.get_field("declaration_type").choices).get(self.declaration_type)
        return f"Declaration {self.declaration_year} ({type_display})"