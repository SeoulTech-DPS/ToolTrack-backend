from django.db import models

# Create your models here.
class Student(models.Model):
    studentId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)