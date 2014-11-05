from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from PrisonerExpress.models import Prison, Prisoner
from django.shortcuts import get_object_or_404, render, redirect


def index(request):
    total = len(Prison.objects.all())
    return HttpResponse("There are %s prisoners in the system" % total)


def details(request, prisoner_id):
    p = Prisoner.objects.get(pk=prisoner_id)
    return HttpResponse("%s has prisoner id of %s" % (p.name, p.id))


def create_prisoner(prisoner_name, prisoner_id,
                    prisoner_address, prison_id, rules):
    if prisoner_name is None:
        raise Exception("Prisoner must have a name")
    if prisoner_id is None:
        raise Exception("Prisoner must have an address")
    if prisoner_address is None and prison_id == -1:
        raise Exception(
            "Prisoner Address and Prison cannot both be unspecified")
    sanitized_id = filter(str.isalnum, prisoner_id)
    prison = None
    if int(prison_id) != -1:
        prison = Prison.objects.get(pk=prison_id)
    address = prisoner_address if len(prisoner_address) > 0 else prison.address
    p = Prisoner(name=prisoner_name,
                 prisoner_id = sanitized_id,
                 prisoner_id_raw = prisoner_id,
                 active=True,
                 prison=prison,
                 address=address,
                 age=-1)
    p.save()
    return p.id


def get_letters(request, prisoner_id):
    prisoner = Prisoner.objects.get(pk=prisoner_id)
    if request.GET['groupby'] == None:
        return Letters.objects.get(prisoner=prisoner)


def create(request):
    if request.method == 'POST':
        new_p = create_prisoner(request.POST['name'],
                                request.POST['prisoner_id'],
                                request.POST['mailing_address'],
                                request.POST['prison'],
                                request.POST['prison_rules'])
        return redirect('prisoner_details', pk=new_p)
    return render(request,
                  "create_prisoner.html",
                  {'prison_list':Prison.objects.all()})


def search(request):
    if ('term' not in request.GET):
        return render(request, "prisoner_search.html")
    search_term = request.GET['term']
    prisoners = Prisoner.objects.filter(prisoner_id__contains=search_term)
    return render(request,
                  "prisoner_list.html",
                  {'object_list': prisoners})


class PrisonerList(ListView):
    template_name='prisoner_list.html'
    model=Prisoner


class PrisonerDetail(DetailView):
    template_name="prisoner_detail.html"
    model=Prisoner


class PrisonerIndex(TemplateView):
    template_name="prisoner_index.html"
