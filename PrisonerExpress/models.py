from django.db import models

# Create your models here.

class Prisoner(models.Model):
	name=models.CharField(max_length=200)
	age=models.IntegerField()

class Program(models.Model):
	name=models.CharField(max_length=200)

	
