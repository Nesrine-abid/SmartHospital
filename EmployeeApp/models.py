from enum import Enum

from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    postalCode = models.CharField(max_length=200)


class Information(models.Model):
    GENDER = (('male', 'male'),
              ('female', 'female'))
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    phone = models.CharField(max_length=50)
    cin = models.CharField(max_length=8)
    passport = models.CharField(max_length=7)
    nationality = models.CharField(max_length=30)
    date_of_Birth = models.DateField()
    gender = models.CharField(max_length=30, choices=GENDER)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    # user_image = models.ImageField()


class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=500)


class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    occupation = models.CharField(max_length=100)
    chronic_disease = models.CharField(max_length=100)
    allergy = models.CharField(max_length=100)
    info_patient = models.OneToOneField(Information, on_delete=models.CASCADE)


class Employee(models.Model):
    ROLE = (('doctor', 'doctor'),
            ('analysist', 'analysist'),
            ('radiologist', 'radiologist'),
            ('pharmacist', 'pharmacist'),
            ('secretary', 'secretary'))
    employeeId = models.AutoField(primary_key=True)
    role = models.CharField(max_length=30, choices=ROLE)
    speciality = models.CharField(max_length=50)
    dateOfJoining = models.DateField()
    info_Employee = models.OneToOneField(Information, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    patients = models.ManyToManyField(Patient, null=True, blank=True, related_name='staff_medical')


class Consultation(models.Model):
    consultationId = models.AutoField(primary_key=True)
    APPOINTMENT_STATE = (('available', 'available'),
                         ('unavailable', 'unavailable'))
    appointmentDate = models.DateField()
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='consultations')
    appointmentState = models.CharField(max_length=30, choices=APPOINTMENT_STATE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    prescriptionImage = models.ImageField(null=True, blank=True)
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
