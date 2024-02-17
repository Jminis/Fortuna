from django import forms
from .models import GameBox, Challenge

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = GameBox
        
        fields = [
            'challenge_id', 'challenge_name', 'team_id', 'description', 
            'visible', 'score', 'is_down', 'is_attacked'
        ]

        widgets = {
            'challenge_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Challenge ID'}),
            'challenge_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Challenge NAME'}),
            'team_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'TEAM ID'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 5, 'placeholder':'Challenge Description'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Score'}),
            'visible': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'is_down': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'is_attacked': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        }

class GameBoxForm(forms.ModelForm):
    class Meta:
        model = Challenge

        fields = [

        ]