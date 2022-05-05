from enum import Enum

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
class File(models.Model):
    fileId = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name



class Address(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    postalCode = models.CharField(max_length=200)



class Information(Address,File):
    GENDER = (('male', 'male'),
              ('female', 'female'))
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=254,unique= True)
    password = models.CharField(max_length=254)
    phone = models.CharField(max_length=50)
    cin = models.CharField(max_length=8,blank=True)
    passport = models.CharField(max_length=7,blank=True)
    nationality = models.CharField(max_length=30)
    date_of_Birth = models.DateField()
    gender = models.CharField(max_length=30, choices=GENDER)
    #address = models.OneToOneField(Address, on_delete=models.CASCADE)
    # user_image = models.ImageField()

class Department(models.Model):
    departmentName = models.CharField(unique=True,max_length=200)

class Patient(models.Model):
    patientId = models.AutoField(primary_key=True)
    occupation = models.CharField(max_length=100)
    chronic_disease = models.CharField(max_length=100)
    allergy = models.CharField(max_length=100)
    info_patient = models.OneToOneField(Information, on_delete=models.CASCADE)

class MyUserManager(BaseUserManager):
        def create_user(self, email,password=None,**otherfields):
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                email=self.normalize_email(email),
                **otherfields
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email,password=None,**otherfields):
            user = self.create_user(
                email,
                password=password,
                **otherfields
            )
            user.is_admin = True
            user.is_staff = True
            user.save(using=self._db)
            return user


class Employee(Information,AbstractBaseUser):
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
    patients = models.ManyToManyField(Patient, null=True, blank=True, related_name='staff_medical')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cin']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class Consultation(models.Model):
    consultationId = models.AutoField(primary_key=True)
    APPOINTMENT_STATE = (('available', 'available'),
                         ('unavailable', 'unavailable'))
    appointmentDate = models.DateField()
    doctor = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='consultations')
    appointmentState = models.CharField(max_length=30, choices=APPOINTMENT_STATE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    prescriptionImage = models.ImageField(upload_to='auth/uploads/consultation_image',null=True,blank=True)
    prescriptionText = models.CharField(max_length=100, null=True, blank=True)
    doctorNotes = models.CharField(max_length=100, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    bloodPressure = models.FloatField(null=True, blank=True)


class Analysis(models.Model):
    AnalysisId = models.AutoField(primary_key=True)
    #analyst = models.OneToOneField(Employee, on_delete=models.CASCADE)
    Analysis_image = models.ImageField()
    AnalystNotes = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)


class Radio(models.Model):
    RadioId = models.AutoField(primary_key=True)
    #radiologist = models.OneToOneField(Employee, on_delete=models.CASCADE)
    radio_image = models.ImageField()
    radiologistNotes = models.CharField(max_length=100)
    doctorNotes = models.CharField(max_length=100)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
