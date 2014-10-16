from django.shortcuts import render
from django.http import HttpResponse

from PrisonerExpress.models import Prison
from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    total = len(Prison.objects.all())
    return HttpResponse("There are %s prisons in the system" % total)


def details(request, prison_id):
    prison = get_object_or_404(Prison, pk=prison_id)
    return HttpResponse("Here are the details for prison %s" % prison)


def create_prison(prison_name, prison_address, prison_rules):
    if prison_name is None or prison_address is None:
        raise Http404
    if prison_rules is None:
        prison_rules = ""
    p = Prison(name=prison_name,
               address = prison_address,
               rules = prison_rules)
    p.save()
    return p.id


def create(request):
    if request.method == 'POST':
        new_prison_id = create_prison(request.POST['prison_name'],
                                      request.POST['prison_address'],
                                      request.POST['prison_rules'])
        return redirect('prison_details', prison_id=new_prison_id)
    return render(request, "create_prison.html")


def edit(request, prison_id):
    return HttpResponse("Edit page for prison %d" % prison_id)


