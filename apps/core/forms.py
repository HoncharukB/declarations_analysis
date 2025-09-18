from django import forms

from apps.core.models import Declarant


class DeclarantForm(forms.ModelForm):
    class Meta:
        model = Declarant
        # 1
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'owner', 'user_declarant_id', 'api_id']

        # 2
        # fields = ['']
        # widgets = {
            # 'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),

        # }