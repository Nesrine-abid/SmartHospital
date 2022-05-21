# Generated by Django 4.0.4 on 2022-05-21 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('consultationId', models.AutoField(primary_key=True, serialize=False)),
                ('appointmentDate', models.DateField()),
                ('appointmentState', models.CharField(choices=[('available', 'available'), ('unavailable', 'unavailable')], max_length=30)),
                ('prescriptionImage', models.ImageField(blank=True, null=True, upload_to='uploads/% Y/% m/% d/')),
                ('prescriptionText', models.CharField(blank=True, max_length=100, null=True)),
                ('doctorNotes', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('bloodPressure', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentName', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('doctor', 'doctor'), ('analysist', 'analysist'), ('radiologist', 'radiologist'), ('pharmacist', 'pharmacist'), ('secretary', 'secretary')], max_length=30)),
                ('speciality', models.CharField(max_length=50)),
                ('dateOfJoining', models.DateField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_staff', to='EmployeeApp.department', to_field='departmentName')),
                ('patients', models.ManyToManyField(blank=True, related_name='staff_medical', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Radio',
            fields=[
                ('RadioId', models.AutoField(primary_key=True, serialize=False)),
                ('radio_image', models.ImageField(upload_to='')),
                ('radiologistNotes', models.CharField(max_length=100)),
                ('doctorNotes', models.CharField(max_length=100)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.consultation')),
                ('radiologist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.employee')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='EmployeeApp.employee'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('AnalysisId', models.AutoField(primary_key=True, serialize=False)),
                ('Analysis_image', models.ImageField(upload_to='')),
                ('AnalystNotes', models.CharField(max_length=100)),
                ('doctorNotes', models.CharField(max_length=100)),
                ('analyst', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.employee')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.consultation')),
            ],
        ),
    ]
