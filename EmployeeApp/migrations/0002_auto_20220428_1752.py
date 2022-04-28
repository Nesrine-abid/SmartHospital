# Generated by Django 2.2.27 on 2022-04-28 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EmployeeApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('consultationId', models.AutoField(primary_key=True, serialize=False)),
                ('appointmentDate', models.DateField()),
                ('appointmentState', models.CharField(choices=[('available', 'available'), ('unavailable', 'unavailable')], max_length=30)),
                ('prescriptionImage', models.ImageField(blank=True, null=True, upload_to='auth/uploads/consultation_image')),
                ('prescriptionText', models.CharField(blank=True, max_length=100, null=True)),
                ('doctorNotes', models.CharField(blank=True, max_length=100, null=True)),
                ('temperature', models.FloatField(blank=True, null=True)),
                ('bloodPressure', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employeeId', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('doctor', 'doctor'), ('analysist', 'analysist'), ('radiologist', 'radiologist'), ('pharmacist', 'pharmacist'), ('secretary', 'secretary')], max_length=30)),
                ('speciality', models.CharField(max_length=50)),
                ('dateOfJoining', models.DateField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.Department')),
            ],
        ),
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='information',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Radio',
            fields=[
                ('RadioId', models.AutoField(primary_key=True, serialize=False)),
                ('radio_image', models.ImageField(upload_to='')),
                ('radiologistNotes', models.CharField(max_length=100)),
                ('doctorNotes', models.CharField(max_length=100)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.Consultation')),
                ('radiologist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='info_Employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.Information'),
        ),
        migrations.AddField(
            model_name='employee',
            name='patients',
            field=models.ManyToManyField(blank=True, null=True, related_name='staff_medical', to='EmployeeApp.Patient'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='EmployeeApp.Employee'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='EmployeeApp.Patient'),
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('AnalysisId', models.AutoField(primary_key=True, serialize=False)),
                ('Analysis_image', models.ImageField(upload_to='')),
                ('AnalystNotes', models.CharField(max_length=100)),
                ('doctorNotes', models.CharField(max_length=100)),
                ('analyst', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.Employee')),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmployeeApp.Consultation')),
            ],
        ),
    ]
