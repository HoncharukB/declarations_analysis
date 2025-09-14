from django.db import models


class BankAccount(models.Model):
    # Звичайні поля
    object_type = models.CharField(max_length=255)
    currency = models.CharField(max_length=10, null=True, blank=True)  # assetsCurrency
    amount = models.PositiveBigIntegerField(null=True, blank=True)  # sizeAssets
    organization = models.CharField(max_length=255, null=True, blank=True) # organization_ua_company_name / organization
    organization_type = models.CharField(max_length=255, null=True, blank=True)  # organization_type1, establishment_type
    organization_ua_company_code = models.CharField(max_length=50, null=True, blank=True)  # organization_ua_company_code
    iteration = models.CharField(max_length=50, null=True, blank=True)  # episode iteration for uniqueness
    extra_info = models.JSONField(null=True, blank=True)  # для додаткової інформації зі структури JSON step_12, step_17
    # Зв'язки
    declarations = models.ManyToManyField("Declaration", related_name='bank_accounts')
    owners = models.ManyToManyField("Owner", related_name='bank_accounts')
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean_confidential(self):
        fields = ['organization', 'organization_type', 'organization_ua_company_code']
        for field in fields:
            val = getattr(self, field)
            if val and '[Конфіденційна інформація]' in val:
                setattr(self, field, None)
        if self.extra_info:
            self.extra_info = self._filter_confidential_in_json(self.extra_info)

    def _filter_confidential_in_json(self, data):
        if isinstance(data, dict):
            return {k: self._filter_confidential_in_json(v) for k, v in data.items() if '[Конфіденційна інформація]' not in str(v)}
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
        org = self.organization or "Організація прихована"
        currency = self.currency or ""
        return (f"BankAccount: {self.object_type} ({amount_str} {currency}) "
                f"Організація: {org}; Власники: [{owners_names}]")