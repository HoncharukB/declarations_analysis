from django import forms

from apps.core.models import Declarant
from apps.core.models.validators.validators import validate_no_digits


class DeclarantForm(forms.ModelForm):
    surname = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
        validators=[validate_no_digits]
    )
    name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
        validators=[validate_no_digits]
    )
    patronymic = forms.CharField(
        label="По батькові",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'По батькові'}),
        validators=[validate_no_digits]
    )

    class Meta:
        model = Declarant
        # 1
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'owner', 'user_declarant_id', 'api_id']
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Населений пункт'}),
            'work_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місце роботи'}),
            'work_post': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Займана посада'}),
            'actual_country': forms.Select(attrs={'class': 'form-control'}),
            'responsible_position': forms.Select(attrs={'class': 'form-control'}),
            'corruption_affected': forms.Select(attrs={'class': 'form-control'}),
            'public_person': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'surname': 'Прізвище',
            'name': "Ім'я",
            'patronymic': 'По батькові',
            'region': 'Населений пункт',
            'work_place': 'Найменування місця роботи або проходження служби (або місця майбутньої роботи чи '
                          'проходження служби для кандидатів)',
            'work_post': 'Займана посада (або посада, на яку претендуєте як кандидат)',
            'actual_country': 'Країна',
            'responsible_position': 'Відповідальне становище',
            'corruption_affected': 'Посада з високим корупційним ризиком',
            'public_person': 'Національний публічний діяч',
        }

        # 2 Якщо потрібно змінити порядок полів
        # fields = ['surname', 'name', 'patronymic', 'actual_country', 'region', 'work_place', 'work_post', 'responsible_position', 'corruption_affected', 'public_person']
        # widgets = {
        #     'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
        #     'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'По батькові'}),
        #     'actual_country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Оберіть країну'}),
        #     'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Населений пункт'}),
        #     'work_place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місце роботи'}),
        #     'work_post': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Займана посада'}),
        #     'responsible_position': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Оберіть становище'}),
        #     'corruption_affected': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Оберіть посаду'}),
        #     'public_person': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Оберіть статус'}),
        #
        # }