# Generated by Django 4.2.7 on 2023-11-26 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_authinfo_team_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authinfo',
            name='team_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
