# Generated by Django 4.0.2 on 2022-05-11 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_corporate_culture_synergymission_culture_and_values_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='synergymission',
            name='mission_similarity',
        ),
    ]
