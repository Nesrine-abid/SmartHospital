from enum import Enum

from django.contrib.auth.models import UserManager
from django.db import models
from users.models import User, Information, Patient


class Department(models.Model):
    departmentName = models.CharField(unique=True,max_length=500)


class Employee(User):
    ROLE = (('doctor', 'doctor'),
            ('analysist', 'analysist'),
            ('radiologist', 'radiologist'),
            ('pharmacist', 'pharmacist'),
            ('secretary', 'secretary'))
    employeeId = models.AutoField(primary_key=True)
    role = models.CharField(max_length=30, choices=ROLE)
    speciality = models.CharField(max_length=50)
    dateOfJoining = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE,to_field="departmentName",blank=True,null=True,related_name='department_staff')
    patients = models.ManyToManyField(Patient, blank=True, related_name='staff_medical')
    is_verified = models.BooleanField(default=False)


class Consultation(models.Model):
    consultationId = models.AutoField(primary_key=True)
    APPOINTMENT_STATE = (('available', 'available'),
                         ('unavailable', 'unavailable'))
    appointmentDate = models.DateField()
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='consultations')
    appointmentState = models.CharField(max_length=30, choices=APPOINTMENT_STATE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    prescriptionImage = models.ImageField(upload_to='uploads/% Y/% m/% d/', null=True, blank=True)
    prescriptionText = models.CharField(max_length=100, null=True, blank=True)
    doctorNotes = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    bloodPressure = models.FloatField(null=True, blank=True)


class Analysis(models.Model):
    AnalysisId = models.AutoField(primary_key=True)
    analyst = models.OneToOneField(Employee, on_delete=models.CASCADE)
    Analysis_image = models.ImageField()
    AnalystNotes = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)


class Radio(models.Model):
    RadioId = models.AutoField(primary_key=True)
    radiologist = models.OneToOneField(Employee, on_delete=models.CASCADE)
    radio_image = models.ImageField()
    radiologistNotes = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
