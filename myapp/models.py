from django.db import models
import datetime 
from django.contrib.auth.models import User
# Create your models here.

class booklist(models.Model):
    img = models.ImageField(upload_to='books', default='books/default.jpg')
    dispo = models.CharField(max_length=100)
    borrowed_book = models.BooleanField(default=False)
    
class userprofile(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='pics',default=False)

class borrower(models.Model):
    name = models.CharField(max_length=1000)
    number = models.IntegerField()


class booktaken(models.Model):   
    bookdispo = models.CharField(max_length=1000)
    taken_at = models.DateTimeField(null=True, blank=True)
    given_at = models.DateTimeField(null=True, blank=True)
    borrower = models.ForeignKey(borrower, on_delete=models.CASCADE)

class recordofediting(models.Model):
    editedby = models.CharField(max_length=100)
    bdispo = models.CharField(max_length=100)
    tdispo =  models.CharField(max_length=100)

class recofremoving(models.Model):
    deletedby = models.CharField(max_length=100) 
    dispo = models.CharField(max_length=100)
    
class permissions(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    addbook = models.BooleanField(default=False)
    addstaff = models.BooleanField(default=False)
    editbooks = models.BooleanField(default=False)
    editstaff = models.BooleanField(default=False)
    recofredited = models.BooleanField(default=False)
    recofdeleted = models.BooleanField(default=False)
    removebook = models.BooleanField(default=False)
    removestaff = models.BooleanField(default=False)
