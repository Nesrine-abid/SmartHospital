from django.db import models


class Patients(models.Model):
    PatientsId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=30)
    LastName = models.CharField(max_length=30)
    Email_Address = models.EmailField(max_length=254)
    Telephone = models.CharField(max_length=8)
    CIN = models.CharField(max_length=8)
    Address = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    Date_of_Birth = models.DateField()
    Occupation = models.CharField(max_length=100)
    Chronic_disease = models.CharField(max_length=100)
    Allergy = models.CharField(max_length=100)


class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=500)


class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=500)
    Department = models.CharField(max_length=500)
    DateOfJoining = models.DateField()
    PhotoFileName = models.CharField(max_length=500)