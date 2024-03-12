from django import forms
from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = ['starttime', 'endtime', 'ctf_name', 'flag_head', 'round_time', 'point_down', 'point_attack', 'point_base', 'db_name', 'db_port', 'db_username', 'db_password']