from django import forms
from django.forms import fields, models
from django.forms.widgets import PasswordInput, TextInput
from users.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'is_staff']

    def save(self, commit):
        self.instance.set_password(self.cleaned_data['password'])
        user = super().save(commit=commit)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(min_length=6, widget=PasswordInput())

