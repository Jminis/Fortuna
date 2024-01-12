# account/forms.py
from django import forms
from .models import Team

# html에서 form.as_p 이런 식으로 사용하면 <p> 태그로 가져올 수 있다는데...
#class LoginForm(forms.Form):
#    name = forms.CharField(label='Team Name', max_length=255)
#    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = Team
        fields = ['name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")