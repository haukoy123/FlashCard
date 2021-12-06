from django import forms
from Cards.models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        widgets = {
            'front': forms.Textarea(attrs={
                'class': 'form-control input_card',
                'rows':'5'
            }),
            'back': forms.Textarea(attrs={
                'class': 'form-control input_card',
                'rows':'5'
            })
        }
