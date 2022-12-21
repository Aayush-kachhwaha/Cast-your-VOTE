from django.db import models
from django.core.validators import MinLengthValidator
import datetime
# Create your models here.

#model for aadhaar database --> can be accessed only by the admin 
class aadhaarDB(models.Model):
    Name = models.CharField(max_length = 100)
    AadhaarNum = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    DOB = models.DateField()
    Mobile = models.CharField(default = '', max_length=10, validators=[MinLengthValidator(10)])
    Age = models.IntegerField(default = None) 
    Gender = models.CharField(max_length = 20)
    State = models.CharField(max_length = 50)
    City = models.CharField(max_length = 50)
    Pincode = models.CharField(max_length = 20)
    Nationality = models.CharField(max_length = 50)

    def __str__(self):
        return self.Name


#model for signup of new users
class registeredUsers(models.Model):
    aadhaar = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    username = models.CharField(max_length=50)
    mobileFromAadhaar = models.BooleanField()
    mobile = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    email = models.EmailField()
    pin = models.CharField(max_length=4, validators=[MinLengthValidator(4)])
    inVotersList = models.BooleanField(default = False)

    def __str__(self):
        aadhaar = self.aadhaar
        db = aadhaarDB.objects.all()
        for objects in db.iterator() :
            if aadhaar == objects.AadhaarNum :
                name = objects.Name
                break
        return name

    def register(self) :
        self.save()
