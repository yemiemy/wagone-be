# Generated by Django 5.0.3 on 2024-03-20 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='mesage',
            new_name='content',
        ),
    ]
