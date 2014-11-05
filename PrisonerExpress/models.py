from django.db import models
from django import forms
from datetime import datetime


class Program(models.Model):
    name=models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    continuous = models.BooleanField(default = True)
    description = models.CharField(max_length=1000, default="N/A")
    def __str__(self):
        return self.name

class Address(models.Model):
    """Class to represent all addresses, thus standardizing address handling code"""
    city = models.CharField(max_length=100) #City
    state = models.CharField(max_length=100) #State
    postal_code = models.CharField(max_length=10) #Room for zip-plus-4
    address_1= models.CharField(max_length=100) #Line 1
    address_2= models.CharField(max_length=100) #Line 2
    address_3= models.CharField(max_length=100) #Line 3
    raw = models.CharField(max_length=200, default="")

    def get_lines(self):
        addr = []
        if (len(self.address_1) >0 ):
            addr.append(self.address_1)
        if (len(self.address_2) >0):
            addr.append(self.address_2)
        if (len(self.address_3) >0):
            addr.append(self.address_3)
        addr.append("%s, %s %s" % (self.city, self.state, self.postal_code))
        return addr

class Prison(models.Model):
    name=models.CharField(max_length=200)
    primary_address=models.ForeignKey(Address)
    rules=models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Prisoner(models.Model):
    name=models.CharField(max_length=200)
    prisoner_id=models.CharField(max_length=80) #santitized version of the id
    prisoner_id_raw=models.CharField(max_length=100) #how the id was entered
    active=models.BooleanField(default=True)
    prison=models.ForeignKey(Prison, null=True)
    programs=models.ManyToManyField(Program, related_name = "prisoners")
    address=models.ForeignKey(Address)
    last_active=models.DateTimeField('last active date', default=datetime.now)

    def __str__(self):
        return "Name: %s | ID: %s " % (self.name, self.prisoner_id)


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
