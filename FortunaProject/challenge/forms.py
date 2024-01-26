from django import forms
from .models import GameBox

class GameBoxForm(forms.ModelForm):
    class Meta:
        model = GameBox
        fields = [
            'challenge_id', 'challenge_name', 'team_id', 'ip', 'port',
            'ssh_port', 'ssh_user', 'ssh_password', 'description', 'visible', 
            'score', 'is_down', 'is_attacked'
        ]
        widgets = {
            'challenge_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Challenge ID'}),
            'challenge_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Challenge NAME'}),
            'team_id': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'TEAM ID'}),
            'ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'IP Address'}),
            'port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Port Number'}),
            'ssh_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'SSH Port Number'}),
            'ssh_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'SSH Username'}),
            'ssh_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'SSH Password'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 5, 'placeholder':'Challenge Description'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Score'}),
            'visible': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'is_down': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'is_attacked': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
        }
