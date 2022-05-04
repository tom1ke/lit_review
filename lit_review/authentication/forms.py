from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput
from django import forms


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].label = ''

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


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs={'class': 'validate', 'placeholder': 'Nom d\'utilisateur'}),
        label='')
    password = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        label='')
