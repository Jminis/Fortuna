from django import forms
from .models import Team

class TeamCreationForm(forms.ModelForm):
    

    class Meta:
        model = Team
        fields = ['name', 'score', 'secret_key', 'team_id', 'token', 'is_staff']
        

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Score'}),
            'secret_key': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Secret Key'}),
            'team_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team ID'}),
            'token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Token'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }

    # 필요한 경우, 여기에 추가적인 유효성 검사 메서드를 정의할 수 있습니다.
    # 예: def clean_<fieldname>(self):
