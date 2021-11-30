from django import forms
from django.forms.widgets import PasswordInput
from users.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import  password_validation



class UserForm(forms.ModelForm):
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
        ),
    )
    email = forms.EmailField(
        error_messages={'unique':"Email  đã được đăng kí."},
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control form-control-sm'
            })
        }
        error_messages = {
            'username': {
                'unique':"Username đã được đăng kí."
            }
        }



    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data['password'])
        user = super().save(commit=commit)
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class PasswordChangeForm(forms.Form):
    def __init__(self, instance=None, *args, **kwargs):
        self.instance = instance
        super().__init__(*args, **kwargs)

    current_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))



class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={'unique':"Email  đã được đăng kí."},
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'is_staff', 'password', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control form-control-sm'
            })
        }
        error_messages = {
            'username': {
                'unique':"Username đã được đăng kí."
            }
        }


class SetPasswordFormCustom(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'style': 'width: 300px;',
            'class': 'form-control'
        }),
    )

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        password_validation.validate_password(new_password, self.user)
        return new_password

        
    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


