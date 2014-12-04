from django.db import models
from django import forms
from datetime import datetime
from widgets import AddressWidget
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Program(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    continuous = models.BooleanField(default = True)
    description = models.CharField(max_length=1000, default="N/A")
    print_rule = models.BooleanField(default = False)
    def __str__(self):
        return self.name

class Address(models.Model):
    """Class to represent all addresses, thus standardizing address handling code"""
    city = models.CharField(max_length=100) #City
    state = models.CharField(max_length=100) #State
    postal_code = models.CharField(max_length=10) #Room for zip-plus-4
    address_1= models.CharField(max_length=100) #Line 1
    address_2= models.CharField(max_length=100) #Line 2
    address_3= models.CharField(max_length=100, default="") #Line 3
    raw = models.CharField(max_length=200, default="")

    class AddressField(forms.Field):
        default_error_message = {
            'invalid': 'Your address could not be parsed'
            }

        widget = AddressWidget

        def to_python(self, value):
            return Address(address_1 = value[0],
                           address_2 = value[1],
                           address_3 = "",
                           city = value[2],
                           state = value[3],
                           postal_code = value[4])

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

    class PrisonForm(forms.Form):
        name=forms.CharField(max_length=100)
        primary_address=Address.AddressField(label="")
        rules=forms.CharField(max_length=300)


class Prisoner(models.Model):
    name=models.CharField(max_length=200)
    prisoner_id=models.CharField(primary_key=True,
                                 max_length=80) #santitized version of the id
    prisoner_id_raw=models.CharField(max_length=100) #how the id was entered
    active=models.BooleanField(default=True)
    prison=models.ForeignKey(Prison, null=True)
    programs=models.ManyToManyField(Program, related_name = "prisoners")
    address=models.ForeignKey(Address)
    last_active=models.DateTimeField('last active date', default=datetime.now)
    rules=models.CharField(max_length=20)
    def __str__(self):
        return "Name: %s | ID: %s " % (self.name, self.prisoner_id)

class PrisonerForm(forms.Form):
    name=forms.CharField(max_length=100)
    prisoner_id=forms.CharField(max_length=100)
    mailing_address=Address.AddressField(label="")
    #prison=forms.CharField(max_length=100)
    rules=forms.CharField(max_length=100)


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
    date=models.DateTimeField(auto_now_add=True, blank=True)
    image=models.ImageField(upload_to='Letters')


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile')
    phone_number = models.CharField(blank=True, default = 'N/A', max_length=20)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Unknown'),
        )
    gender=models.CharField(max_length=2,
                                   choices=GENDER_CHOICES,
                                   default='N')
    is_volunteer = models.BooleanField(default = False);
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user','is_volunteer']

