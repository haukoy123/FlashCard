from django import forms
from django.forms.forms import Form
from django.forms.widgets import PasswordInput
from users.models import User
from django.forms.utils import ErrorList



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
        exclude = ['is_superuser', 'last_login', 'is_staff']
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


    # REVIEW: khi ghi đè, chú ý giữ đúng signature của hàm mình đang ghi đè
    # hoặc dùng *args, **kwargs
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
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, use_required_attribute=None,
                 renderer=None):
        self.instance = instance
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                initial=initial, error_class=error_class, label_suffix=label_suffix,
                empty_permitted=empty_permitted, use_required_attribute=use_required_attribute, renderer=renderer)

    current_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))

    def save(self):
        self.instance.set_password(self.cleaned_data['password'])
        self.instance.save()
        return self.instance



class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        error_messages={'unique':"Email  đã được đăng kí."},
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        exclude = ['is_superuser', 'last_login', 'is_staff', 'password']
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