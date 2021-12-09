from django import forms
from Cards.models import Card


class CardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card_group'].disabled = True
        

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
            }),
            'card_group': forms.TextInput(attrs={'hidden': 'True;'})
        }
