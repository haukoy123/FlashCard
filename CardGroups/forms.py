from users.models import User
from CardGroups.models import CardGroup
from django import forms
import datetime

class DurationFieldCustom(forms.DurationField):

    def prepare_value(self, value):
        if isinstance(value, datetime.timedelta):
            value = value.seconds / 60
        return value


    def to_python(self, value):
        try:
            study_duration_minute = int(value)
        except ValueError as e:
            return super().to_python(value)

        value = datetime.timedelta(seconds=study_duration_minute * 60)
        return super().to_python(value)



class CardGroupForm(forms.ModelForm, DurationFieldCustom):

    user = forms.ModelChoiceField(User.objects.all(), required=False, disabled=True)
    study_duration = DurationFieldCustom(
        error_messages={'invalid':'Phải nhập số nguyên dương(đơn vị phút)'},
        widget=forms.NumberInput(
            attrs={'class': 'form-control bg-input-group'}
        )
    )
    class Meta:
        model = CardGroup
        exclude = ['last_study_at', 'study_count']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-input-group'
            })
        }



    # def clean_study_duration(self):
    #     # REVIEW: đoạn này đọc hơi lạ, lấy "seconds" nhưng lại set vào "minutes"
    #     study_duration_minute = self.cleaned_data['study_duration'].seconds
    #     return timedelta(seconds=study_duration_minute*60)
