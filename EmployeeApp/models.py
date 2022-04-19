from enum import Enum
from django.db import models
from django.db.models import ManyToManyField


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


#     #staffList = ListField(Employee)


class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    occupation = models.CharField(max_length=100)
    chronic_disease = models.CharField(max_length=100)
    allergy = models.CharField(max_length=100)
    info_patient = models.OneToOneField(Information, on_delete=models.CASCADE)


class Employee(models.Model):
    ROLE = (('doctor', 'doctor'),
              ('analysist', 'analysist'),
              ('biologist', 'biologist'),
              ('pharmacist', 'pharmacist'),
              ('secretary', 'secretary'))
    employeeId = models.AutoField(primary_key=True)
    role = models.CharField(max_length=30, choices=ROLE)
    speciality = models.CharField(max_length=50)
    dateOfJoining = models.DateField()
    info_Employee = models.OneToOneField(Information, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    #patients = models.ManyToManyField(Patient)

# class Appointment(models.Model):
#     APPOINTMENT_STATE = (('available','available'),
#                         ('unavailable','unavailable'))
#
#     appointmentId = models.AutoField(primary_key=True)
#     appointmentDate = models.DateField()
#     doctor = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     appointmentState = models.CharField(max_length=30, choices=APPOINTMENT_STATE)
#
#
#
#
#
#
#
# class Consultation(models.Model):
#     consultationId = models.AutoField(primary_key=True)
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     prescriptionImage = models.ImageField()
#     prescriptionText = models.CharField(max_length=100)
#     doctorNotes = models.CharField(max_length=100)
#     temperature = models.FloatField()
#     bloodPressure = models.FloatField()
#     # analysisList = models.ManyToManyField(Analysis)
#     # radioList = models.ManyToManyField(Radio)
#
#
# class Analysis(models.Model):
#     AnalysisId = models.AutoField(primary_key=True)
#     analyst = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     analysis_consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
#     Analysis_image = models.ImageField()
#     AnalystNotes = models.CharField(max_length=100)
#     doctorNotes = models.CharField(max_length=100)
#
#
#
# class Radio(models.Model):
#     RadioId = models.AutoField(primary_key=True)
#     radiologist = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     radio_image = models.ImageField()
#     radio_consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
#     radiologistNotes = models.CharField(max_length=100)
#     doctorNotes = models.CharField(max_length=100)
