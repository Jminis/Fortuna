# Generated by Django 5.0.1 on 2024-01-26 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0012_actiontry_attacker_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='actiontry',
            name='round',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]