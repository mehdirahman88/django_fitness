# Generated by Django 4.2.3 on 2023-07-12 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dietrecord',
            old_name='fitness_user',
            new_name='fitness_user_id',
        ),
    ]
