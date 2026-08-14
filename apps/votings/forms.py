from django import forms

from .models import Voting


class VotingForm(forms.ModelForm):
    options = forms.CharField(
        label='Варіанти відповідей',
        help_text='Щонайменше два варіанти, кожен з нового рядка.',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
    )

    class Meta:
        model = Voting
        fields = ('title', 'description', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_options(self):
        options = [value.strip() for value in self.cleaned_data['options'].splitlines() if value.strip()]
        if len(options) < 2:
            raise forms.ValidationError('Додайте щонайменше два варіанти.')
        if len(options) != len(set(options)):
            raise forms.ValidationError('Варіанти не повинні повторюватися.')
        return options
