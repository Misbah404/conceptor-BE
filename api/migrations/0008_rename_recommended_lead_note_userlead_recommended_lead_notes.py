# Generated by Django 4.0.2 on 2022-03-30 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_userlead_recommended_lead_notes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlead',
            old_name='recommended_lead_note',
            new_name='recommended_lead_notes',
        ),
    ]
