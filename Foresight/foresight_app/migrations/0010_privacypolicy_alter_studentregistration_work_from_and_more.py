# Generated by Django 5.2 on 2025-05-04 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foresight_app', '0009_alter_studentregistration_work_from_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='work_from',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='work_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
