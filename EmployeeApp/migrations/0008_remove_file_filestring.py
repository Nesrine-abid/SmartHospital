# Generated by Django 2.2.27 on 2022-04-30 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0007_auto_20220430_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='fileString',
        ),
    ]
