from django.db import models

# Create your models here.
class Guestbook(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    contents = models.CharField(max_length=200)
    regdate = models.DateTimeField(auto_now=True)