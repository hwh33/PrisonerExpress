from django.shortcuts import render
from django.http import HttpResponse

from PrisonerExpress.models import Prison, Prisoner
from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    total = len(Prison.objects.all())
    return HttpResponse("There are %s prisoners in the system" % total)


def create_prisoner(prisoner_name, prisoner_address, prison_id, rules):
    if prisoner_name is None:
        raise Exception("Prisoner must have a name")
    if prisoner_address is None and prison_id == -1:
        raise Exception("Prisoner Address and Prison cannot both be unspecified")

    prison = None
    if prison_id != -1:
        prison = Prison.objects.get(pk=prison_id)
    address = prisoner_address if prisoner_address is not None else Prison.address
    p = Prisoner(name=prisoner_name,
                 active=True,
                 prison=prison,
                 address=address,
                 age=-1)
    p.save()
    return p.id
                 

def create(request):
    if request.method == 'POST':
        new_p = create_prisoner(request.POST['name'], request.POST['mailing_address'],
                                request.POST['prison'], request.POST['prison_rules'])
        return HttpResponse("Created a new prisoner with id %s" % new_p)
    return render(request, "create_prisoner.html", {'prison_list':Prison.objects.all()})
