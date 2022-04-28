from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Create your models here.


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
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)
    phone = models.CharField(max_length=50)
    cin = models.CharField(max_length=8)
    passport = models.CharField(max_length=7)
    nationality = models.CharField(max_length=30)
    date_of_Birth = models.DateField()
    gender = models.CharField(max_length=30, choices=GENDER)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    # user_image = models.ImageField(null=True,blank=True)


class MyUserManager(BaseUserManager):
    def create_user(self, email, cin, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            cin= cin
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,cin, password=None):
        user = self.create_user(
            email,
            password=password,
            cin= cin
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(Information,AbstractBaseUser):
    occupation = models.CharField(max_length=100)
    chronic_disease = models.CharField(max_length=100)
    allergy = models.CharField(max_length=100)
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

