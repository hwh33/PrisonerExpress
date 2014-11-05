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
        raw_id=request.GET['id'];
        parsed_id = filter(str.isalnum, str(raw_id))
        p = Prisoner(name=first_name+' '+last_name,
                 active=True,
                 address=address,
#                 city=city,
#                 state=state,
#                 zipcode=zipcode,
                     prisoner_id=parsed_id,
                     prisoner_id_raw = parsed_id)
        p.save()
        return HttpResponse("%s has prisoner id of %s" % (p.name, p.id))
