# Generated by Django 4.0.4 on 2022-04-21 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0004_employee_patients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='patients',
        ),
    ]
