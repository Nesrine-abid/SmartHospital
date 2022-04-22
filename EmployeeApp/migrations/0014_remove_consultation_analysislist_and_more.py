# Generated by Django 4.0.4 on 2022-04-22 11:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0013_remove_appointment_doctor_appointment_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='analysisList',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='radioList',
        ),
        migrations.AddField(
            model_name='analysis',
            name='consultation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.consultation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='information',
            name='user_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='radio',
            name='consultation',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.consultation'),
            preserve_default=False,
        ),
    ]
