# Generated by Django 4.0.3 on 2022-04-06 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0005_patients_telephone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patients',
            old_name='Sexe',
            new_name='Gender',
        ),
    ]
