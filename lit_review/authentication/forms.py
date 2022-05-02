from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Mot de passe',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer mot de passe',
                                widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
