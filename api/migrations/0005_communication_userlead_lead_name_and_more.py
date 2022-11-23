# Generated by Django 4.0.2 on 2022-03-24 02:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_merge_20220315_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_company_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userlead',
            name='lead_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]