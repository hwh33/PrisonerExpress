from django.test import TestCase
from PrisonerExpress.models import Prison, Prisoner
from django.http import HttpResponse
# Create your tests here.

def input(request):

	first_name=request.GET['first_name'];
	last_name=request.GET['last_name'];
	address=request.GET['addr'];
	pre_address=request.GET['preaddr'];
	city=request.GET['city'];
	state=request.GET['state'];
	zipcode=request.GET['zipcode'];
	ID=request.GET['id'];
	p = Prisoner(name=first_name+' '+last_name,
                 active=True,
                 address=address,
                 pre_address=pre_address,
                 city=city,
                 state=state,
                 zipcode=zipcode,
                 prisonerID=ID,
                 age=-1)
	p.save()
	return HttpResponse("%s has prisoner id of %s" % (p.name, p.id))
	