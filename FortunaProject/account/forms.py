from django import forms
from .models import Team

class TeamCreationForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'password','score', 'team_id', 'token', 'is_staff']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Score'}),
            'team_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team ID'}),
            'token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Token'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-label'}),   
        }

class AdminTeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'password']  # 관리자가 변경할 수 있는 필드 목록

    def save(self, commit=True):
        team = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            team.set_password(password)
        if commit:
            team.save()
        return team