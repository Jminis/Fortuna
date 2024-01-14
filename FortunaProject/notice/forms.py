from django import forms
from .models import Notices

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'content': forms.Textarea(attrs={'class': 'textarea'}),
        }
