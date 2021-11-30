from CardGroups.models import CardGroup
from django import forms
from datetime import timedelta


class CardGroupForm(forms.ModelForm):
    class Meta:
        model = CardGroup
        exclude = ['last_study_at', 'study_count']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'study_duration': forms.NumberInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_study_duration(self):
        # REVIEW: đoạn này đọc hơi lạ, lấy "seconds" nhưng lại set vào "minutes"
        study_duration_minute = self.cleaned_data['study_duration'].seconds
        return timedelta(minutes=study_duration_minute)

