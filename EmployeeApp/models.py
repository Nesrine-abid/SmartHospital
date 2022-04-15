from enum import Enum
from django.db import models
from django.db.models import ManyToManyField


# class Address(models.Model):
#     addressId = models.AutoField(primary_key=True)
#     country = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     street = models.CharField(max_length=200)
#     postalCode = models.CharField(max_length=200)


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
    gender = models.CharField(max_length=30,choices=GENDER)
   # address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # user_image = models.ImageField(upload_to=images/patient/)


class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=500)
    #staffList = ListField(Employee)


class Patient(Information):
    patientsId = models.AutoField(primary_key=True)
    Occupation = models.CharField(max_length=100)
    Chronic_disease = models.CharField(max_length=100)
    Allergy = models.CharField(max_length=100)

    # class Meta:
    #     proxy = True
    # consultations = ManyToManyField(Consultation)
    # appointments = ManyToManyField(Appointment)

class Employee(models.Model):
    employeeId = models.AutoField(primary_key=True)
    # infoEmployee = models.ForeignKey(Information, on_delete=models.CASCADE)
    Role = models.CharField(max_length=50)
    speciality = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    dateOfJoining = models.DateField()
    patients = ManyToManyField(Patient)
    #
    # class Meta:
    #     proxy = True


class Appointment(models.Model):
    APPOINTMENT_STATE = (('available','available'),
                        ('unavailable','unavailable'))

    appointmentId = models.AutoField(primary_key=True)
    appointmentDate = models.DateField()
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    appointmentState = models.CharField(max_length=30, choices=APPOINTMENT_STATE)







class Consultation(models.Model):
    consultationId = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescriptionImage = models.ImageField()
    prescriptionText = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)
    temperature = models.FloatField()
    bloodPressure = models.FloatField()
    # analysisList = models.ManyToManyField(Analysis)
    # radioList = models.ManyToManyField(Radio)


class Analysis(models.Model):
    AnalysisId = models.AutoField(primary_key=True)
    analyst = models.ForeignKey(Employee, on_delete=models.CASCADE)
    analysis_consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    Analysis_image = models.ImageField()
    AnalystNotes = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)



class Radio(models.Model):
    RadioId = models.AutoField(primary_key=True)
    radiologist = models.ForeignKey(Employee, on_delete=models.CASCADE)
    radio_image = models.ImageField()
    radio_consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    radiologistNotes = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)











