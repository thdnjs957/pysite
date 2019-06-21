from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=32)
    gender = models.CharField(max_length=10)
    joindate = models.DateTimeField(auto_now=True)




