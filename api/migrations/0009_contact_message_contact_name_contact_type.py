# Generated by Django 4.0.2 on 2022-04-07 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_recommended_lead_note_userlead_recommended_lead_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
