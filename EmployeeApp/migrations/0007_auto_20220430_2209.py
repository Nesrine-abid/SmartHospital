# Generated by Django 2.2.27 on 2022-04-30 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0006_auto_20220430_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='fileString',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
