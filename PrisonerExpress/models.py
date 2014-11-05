from django.db import models
from django import forms
from datetime import datetime
# Create your models here.

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
    name=models.CharField(max_length=200)
    active=models.BooleanField(default=True)
    prison=models.ForeignKey(Prison, null=True)
    programs=models.ManyToManyField(Program, related_name = "prisoners")
    address=models.CharField(max_length=200,default="")
    pre_address=models.CharField(max_length=200,default="")
    city=models.CharField(max_length=20,default="")
    state=models.CharField(max_length=5,default="")
    zipcode=models.CharField(max_length=10,default="")
    age=models.IntegerField()
    prisonerID=models.CharField(max_length=20,default="")
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
    prisoner=models.ForeignKey(Prisoner, related_name = "letters")
    program=models.ForeignKey(Program, related_name = "letters")
    content=models.TextField()
    image=models.ImageField(upload_to='Letters')

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
