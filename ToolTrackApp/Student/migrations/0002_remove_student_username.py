# Generated by Django 4.2 on 2024-05-27 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='username',
        ),
    ]