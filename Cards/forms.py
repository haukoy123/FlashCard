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
                'rows':'5',
                'data-bs-trigger': 'focus',
                'data-bs-toggle': 'popover',
                'data-bs-content': '''- Ctrl + Enter nếu card này là card cuối cùng.
                                    <br />
                                    - AltKey + Enter nếu bạn muốn thêm nhiều card khác.''',
                'data-bs-html': 'true'
            
            }),
            'back': forms.Textarea(attrs={
                'class': 'form-control input_card',
                'rows':'5',
                'data-bs-trigger': 'focus',
                'data-bs-toggle': 'popover',
                'data-bs-content': '''- Ctrl + Enter nếu card này là card cuối cùng.
                                    <br />
                                    - AltKey + Enter nếu bạn muốn thêm nhiều card khác.''',
                'data-bs-html': 'true'
            }),
            'card_group': forms.TextInput(attrs={'hidden': 'True;'})
        }
