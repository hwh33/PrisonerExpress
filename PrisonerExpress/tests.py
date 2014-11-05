from django.test import TestCase
from PrisonerExpress.models import Prison, Prisoner, Address
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
        a = Address(city=city, state=state,
                    postal_code=str(int(zipcode)),
                    address_1=pre_address,
                    address_2=address)
        a.save()
        raw_id=request.GET['id'];
        parsed_id = filter(str.isalnum, str(raw_id))
        p = Prisoner(name=first_name+' '+last_name,
                     active=True,
                     address=a,
                     prisoner_id=parsed_id,
                     prisoner_id_raw = raw_id)
        p.save()
        return HttpResponse("%s has prisoner id of %s" % (p.name, p.id))
