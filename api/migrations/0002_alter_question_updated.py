# Generated by Django 4.0.3 on 2022-03-04 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 3, 4, 8, 39, 40, 449941)),
        ),
    ]
