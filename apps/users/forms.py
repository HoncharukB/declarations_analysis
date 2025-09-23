from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.users.models import CustomUser


class CustomeUserCreationForm(UserCreationForm):
    # class Meta(UserCreationForm.Meta):
    class Meta:
        model = CustomUser
        # fields = ('photo', 'username', 'email', 'password1', 'password2')
        fields = ('last_name', 'first_name', 'username', 'email', 'phone', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }