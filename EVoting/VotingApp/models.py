from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.


#model for status of election --> ongoing or completed
class Status(models.Model):
    choices = [('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Upcoming', 'Upcoming')]
    status = models.CharField(choices = choices, max_length = 10)

    def __str__(self):
        return self.status


#model for defining locality of election
class Election_category(models.Model):
    category = models.CharField(max_length = 50)
    status = models.ForeignKey(Status, on_delete = models.CASCADE, default = '')

    def __str__(self):
        return self.category


#model for candidate registration --> can only be modified by the admin side
class Election(models.Model):
    party = models.CharField(max_length = 20)
    candidate_name = models.CharField(max_length = 50)
    category = models.ForeignKey(Election_category, on_delete = models.CASCADE)
    status = models.ForeignKey(Status, on_delete = models.CASCADE)
    logo = models.ImageField(max_length = 100, upload_to = 'VotingApp/static/media/candidates')
    agenda = models.CharField(max_length = 500, default = '')

    def show_all():
        return Election.objects.all()


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
    mobile = models.CharField(max_length=13, validators=[MinLengthValidator(13)])
    mobile_verified = models.BooleanField(default = False)
    aadhaar_verified = models.BooleanField(default = False)
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
