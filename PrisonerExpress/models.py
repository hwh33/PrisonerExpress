from django.db import models
from datetime import datetime


class Program(models.Model):
    name=models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    continuous = models.BooleanField(default = True)
    description = models.CharField(max_length=1000, default="N/A")
    def __str__(self):
        return self.name

class Prison(models.Model):
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    rules=models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Prisoner(models.Model):
    name=models.CharField(max_length=100)
    prisoner_id=models.CharField(max_length=80) #santitized version of the id
    prisoner_id_raw=models.CharField(max_length=100) #how the id was entered
    active=models.BooleanField(default=True)
    prison=models.ForeignKey(Prison, null=True)
    programs=models.ManyToManyField(Program, related_name = "prisoners")
    address=models.CharField(max_length=200,default="")
    age=models.IntegerField()
    last_active=models.DateTimeField('last active date', default=datetime.now)

    def __str__(self):
        return self.name


class Material(models.Model):
    name=models.CharField(max_length=200)
    program=models.ForeignKey(Program, related_name = "materials")
    MATERIAL_TYPE_CHOICES = (
        ('BO', 'Book'),
        ('MA', 'Magazine'),
        ('MO', 'Movie'),
        ('TV', 'TV Show'),
        ('PO', 'Poem'),
        ('SS', 'Short Story'),
        ('PH', 'Word or Phrase'),
        ('PI', 'Picture'),
        ('OO', 'Other')
        )
    material_type=models.CharField(max_length=2,
                                   choices=MATERIAL_TYPE_CHOICES,
                                   default='BO')


class Letter(models.Model):
    prisoner=models.ForeignKey(Prisoner)
    content=models.TextField()
    program=models.ForeignKey(Program, related_name = "letters")
