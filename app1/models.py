from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
# from django.contrib.auth.models import User


# Create your models here.
	
class User(models.Model):
    UserID=models.AutoField(primary_key=True)
    FirstName=models.CharField(max_length=255)
    LastName=models.CharField(max_length=255)
    ProfilePicture=models.FileField( upload_to='profilepicture')
    UserName=models.CharField(max_length=255)
    Email=models.EmailField(max_length=255)
    Address=models.CharField(max_length=255)
    UserType=models.CharField( max_length=255)
    Password=models.CharField( max_length=255)
    ConfirmPassword=models.CharField( max_length=255)
    
	
class Blog(models.Model):
    Title=models.CharField(max_length=250)
    BlogImages=models.FileField( upload_to='blogimg')
    Category=models.CharField( max_length=250)
    Summary=models.CharField( max_length=1000)
    Content=models.CharField(max_length=1000)
    IsDraft= models.BooleanField(default=False)

class Appointment(models.Model):
    DoctorID=models.ForeignKey("app1.User", on_delete=models.CASCADE)
    PatientID=models.BigIntegerField()
    DoctorName=models.CharField(max_length=250)
    Speciality=models.CharField(max_length=250)
    AppointDate=models.DateField()
    AppointStart=models.TimeField()
    AppointEnd=models.CharField(max_length=250)
    PatientName=models.CharField(max_length=250)

# class Message(models.Model):
#     sender = models.ForeignKey("app1.User", on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey("app1.User", on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     SenderName=models.CharField(max_length=250)
#     ReceiverName=models.CharField(max_length=250)
#     DoctorID=models.BigIntegerField()
#     PatientID=models.BigIntegerField()
#     def __str__(self):
#         return f"From {self.sender} to {self.recipient}: {self.content}"

class Room(models.Model):
    RoomName=models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=1000)
    # date = models.DateTimeField(default=datetime.now)
    user = models.CharField(max_length=1000)
    room = models.CharField(max_length=1000)
    # DrUser = models.CharField(max_length=1000)
    # PtUser=models.CharField(max_length=1000)