from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Address(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    postalCode = models.CharField(max_length=200)


class Information(Address, models.Model):
    informationId = models.AutoField(primary_key=True)
    GENDER = (('male', 'male'),
              ('female', 'female'))
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)
    phone = models.CharField(max_length=50,unique=True)
    cin = models.CharField(max_length=8,unique=True,blank=True)
    passport = models.CharField(max_length=7, blank=True)
    nationality = models.CharField(max_length=30)
    date_of_Birth = models.DateField(blank=True)
    gender = models.CharField(max_length=30, choices=GENDER)
    user_image = models.ImageField(null=True, blank=True, upload_to="images/")


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **otherfields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **otherfields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **otherfields):
        user = self.create_user(
            email,
            password=password,
            **otherfields
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(Information, AbstractBaseUser):
    patientId = models.AutoField(primary_key=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=200, null=True,blank=True)
    occupation = models.CharField(max_length=100)
    chronic_disease = models.CharField(max_length=100,blank=True)
    allergy = models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
