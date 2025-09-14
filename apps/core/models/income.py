from django.db import models


class Income(models.Model):
    # Звичайні поля
    object_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # sizeIncome
    source_ua_company_name = models.CharField(max_length=255, null=True, blank=True)
    income_source = models.CharField(max_length=50, null=True, blank=True)  # incomeSource
    source_citizen = models.CharField(max_length=255, null=True, blank=True)
    source_ua_company_code = models.CharField(max_length=50, null=True, blank=True)  # source_ua_company_code
    iteration = models.CharField(max_length=50, null=True, blank=True)  # iteration from sources
    # поле JSON для додаткових/нестандартних даних
    extra_info = models.JSONField(null=True, blank=True)
    # Зв'язки
    declarations = models.ManyToManyField("Declaration", related_name='incomes')
    owners = models.ManyToManyField("Owner", related_name='incomes')
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean_confidential(self):
        fields = ['source_ua_company_name', 'income_source', 'source_citizen', 'source_ua_company_code']
        for field in fields:
            val = getattr(self, field)
            if val and '[Конфіденційна інформація]' in val:
                setattr(self, field, None)

        # Фільтрація json поля extra_info
        if self.extra_info:
            self.extra_info = self._filter_confidential_in_json(self.extra_info)

    def _filter_confidential_in_json(self, data):
        if isinstance(data, dict):
            return {k: self._filter_confidential_in_json(v) for k, v in data.items() if
                    '[Конфіденційна інформація]' not in str(v)}
        elif isinstance(data, list):
            return [self._filter_confidential_in_json(x) for x in data if '[Конфіденційна інформація]' not in str(x)]
        else:
            return data

    def save(self, *args, **kwargs):
        self.clean_confidential()
        super().save(*args, **kwargs)

    def __str__(self):
        owners_names = ', '.join(
            " ".join(filter(None, [owner.last_name, owner.first_name, owner.middle_name])) or "Невідомий"
            for owner in self.owners.all()
        )
        amount_str = f"{self.amount}" if self.amount is not None else "Без суми"
        source = self.source_ua_company_name or "Джерело приховане"
        return (f"Income: {self.object_type} ({amount_str}) from {source}; "
                f"Owners: [{owners_names}]")