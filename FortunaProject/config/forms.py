from django import forms
from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = [
            'starttime', 
            'endtime', 
            'ctf_name', 
            'flag_head', 
            'round_time', 
            'point_down', 
            'point_attack', 
            'point_base'
        ]
        widgets = {
            'starttime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'endtime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'ctf_name': forms.TextInput(attrs={'class': 'form-control'}),
            'flag_head': forms.TextInput(attrs={'class': 'form-control'}),
            'round_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'point_down': forms.NumberInput(attrs={'class': 'form-control'}),
            'point_attack': forms.NumberInput(attrs={'class': 'form-control'}),
            'point_base': forms.NumberInput(attrs={'class': 'form-control'}),
        }
