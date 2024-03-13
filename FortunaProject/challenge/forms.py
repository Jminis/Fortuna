from django import forms
from .models import Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        
        fields = [
            'challenge_id', 'challenge_name', 'description'
        ]

        widgets = {
            'challenge_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Challenge ID'}),
            'challenge_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Challenge NAME'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 5, 'placeholder':'Challenge Description'}),
        }