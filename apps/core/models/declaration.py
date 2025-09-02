from django.db import models

class Declaration(models.Model):
    document_id = models.CharField(max_length=100, unique=True)
    user_declarant_id = models.IntegerField()
    declaration_year = models.IntegerField()
    declaration_type = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f'Declaration {self.declaration_year} date {self.date}, type: {self.declaration_type}'