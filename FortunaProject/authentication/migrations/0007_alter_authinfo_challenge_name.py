# Generated by Django 5.0.1 on 2024-01-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_rename_name_authinfo_challenge_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authinfo',
            name='challenge_name',
            field=models.CharField(max_length=255),
        ),
    ]
