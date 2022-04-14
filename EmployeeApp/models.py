from enum import Enum
from django.db import models
from rest_framework.fields import ListField


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'


class Address(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    postelCode = models.CharField(max_length=200)


class Information(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    password = models.CharField(widget=models.PasswordInput)
    phone = models.CharField(max_length=50)
    cin = models.CharField(max_length=8)
    passport = models.CharField(max_length=7)
    nationality = models.CharField(max_length=30)
    date_of_Birth = models.DateField()
    gender = models.EnumField(Gender)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # user_image = models.ImageField(upload_to=images/patient/)


class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=500)
    #staffList = ListField(Employee) !!!!!!!


class Employee(models.Model):
    employeeId = models.AutoField(primary_key=True)
    infoEmployee = models.ForeignKey(Information, on_delete=models.CASCADE)
    Role = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    dateOfJoining = models.DateField()
    #PatientsList = ListField(Patient) !!!!!!


class AppointmentState(Enum):
    ACCEPTED = 'accepted'
    REFUSED = 'refused'
    WAITING = 'waiting'


class Appointment:
    appointmentId = models.AutoField(primary_key=True)
    appointmentDate = models.DateField()
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    appointmentState = models.EnumField(AppointmentState)


class Analysis:
    AnalysisId = models.AutoField(primary_key=True)
    analyst = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Analysis_image = models.ImageField()
    AnalystNotes = models.CharField()
    doctorNotes = models.CharField()


class Radio:
    RadioId = models.AutoField(primary_key=True)
    radiologist = models.ForeignKey(Employee, on_delete=models.CASCADE)
    radio_image = models.ImageField()
    radiologistNotes = models.CharField()
    doctorNotes = models.CharField()


class Consultation:
    consultationId = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    analysisList = models.ListField(Analysis)
    radioList = models.ListField(Radio)
    prescriptionImage = models.ImageField()
    prescriptionText = models.CharField()
    doctorNotes = models.CharField()
    temperature = models.FloatField()
    bloodPressure = models.FloatField()


class Patient(models.Model):
    patientsId = models.AutoField(primary_key=True)
    infoPatient = models.ForeignKey(Information, on_delete=models.CASCADE)
    Occupation = models.CharField(max_length=100)
    Chronic_disease = models.CharField(max_length=100)
    Allergy = models.CharField(max_length=100)
    consultations = ListField(Consultation)
    appointments = ListField(Appointment)
    medical_staff_Patient = ListField(Employee)

#class GenderPatient(models.TextChoices):
    #MALE = 'M', _('male')
    #FEMALE = 'F', _('female')