from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = '__all__'



    def clean(self):
        cleaned_data = super().clean()
        st = cleaned_data['start_age']
        end = cleaned_data['end_age']
        growth = cleaned_data['growth']
        if not st and not end:
            raise forms.ValidationError({
                'start_age':'Please select either a starting or ending age.',
                'end_age':'Please select either a starting or ending age.',
                })

        if st != None and end != None and st > end :
            raise forms.ValidationError({
                'start_age':'The start age must be less than the end age.',
                'end_age':'The start age must be less than the end age.'
                })
        if st == 65 and growth:
            raise forms.ValidationError({
                'growth':'The start age must be less than 65 for you to add growth',
                })

        return cleaned_data

