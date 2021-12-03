from users.models import User
from CardGroups.models import CardGroup
from django import forms
from datetime import timedelta


class CardGroupForm(forms.ModelForm):

    user = forms.ModelChoiceField(User.objects.all(), required=False, disabled=True)
    class Meta:
        model = CardGroup
        exclude = ['last_study_at', 'study_count']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-input-group'
            }),
            'study_duration': forms.NumberInput(attrs={
                'class': 'form-control bg-input-group'
            })
        }

    

    def clean_study_duration(self):
        # REVIEW: đoạn này đọc hơi lạ, lấy "seconds" nhưng lại set vào "minutes"
        study_duration_minute = self.cleaned_data['study_duration'].seconds
        return timedelta(minutes=study_duration_minute)

