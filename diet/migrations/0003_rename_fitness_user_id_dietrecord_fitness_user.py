# Generated by Django 4.2.3 on 2023-07-12 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0002_rename_fitness_user_dietrecord_fitness_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dietrecord',
            old_name='fitness_user_id',
            new_name='fitness_user',
        ),
    ]
