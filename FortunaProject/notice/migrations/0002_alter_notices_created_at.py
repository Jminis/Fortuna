<<<<<<< HEAD
# Generated by Django 4.2.1 on 2024-01-16 02:07

import datetime
=======
# Generated by Django 5.0.1 on 2024-01-16 18:26

>>>>>>> main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notices',
            name='created_at',
<<<<<<< HEAD
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 16, 2, 7, 13, 422090, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
=======
            field=models.DateTimeField(auto_now_add=True),
>>>>>>> main
        ),
    ]
