# Generated by Django 5.0.1 on 2024-01-16 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_authinfo_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authinfo',
            old_name='name',
            new_name='challenge_name',
        ),
    ]