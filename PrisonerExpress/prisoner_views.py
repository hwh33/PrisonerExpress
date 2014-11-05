from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from PrisonerExpress.models import Prison, Prisoner, PrisonerForm
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


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
    prisoner_address.save()
    prisoner_id = str(prisoner_id)
    sanitized_id = filter(str.isalnum, prisoner_id)
    prison = None
    if int(prison_id) != -1:
        prison = Prison.objects.get(pk=prison_id)
    p = Prisoner(name=prisoner_name,
                 prisoner_id = sanitized_id,
                 prisoner_id_raw = prisoner_id,
                 active=True,
                 prison=prison,
                 address=prisoner_address)
    p.save()
    return p.prisoner_id


def get_letters(request, prisoner_id):
    prisoner = Prisoner.objects.get(pk=prisoner_id)
    if request.GET['groupby'] == None:
        return Letters.objects.get(prisoner=prisoner)


def create(request):
    if request.method == 'POST':
        form = PrisonerForm(request.POST)
        if (form.is_valid()):
            new_p = create_prisoner(form.cleaned_data['name'],
                                form.cleaned_data['prisoner_id'],
                                form.cleaned_data['mailing_address'],
                                -1, #form.cleaned_data['prison'],
                                form.cleaned_data['prison_rules'])
            return redirect('prisoner_details', pk=new_p)
        print "Form not valid"
    return render(request,
                  "create_prisoner_form.html",
                  {'form':PrisonerForm()})


def search(request):
    if ('term' not in request.GET):
        return render(request, "prisoner_search.html")
    search_term = filter(str.isalnum, str(request.GET['term']))
    paginator = Paginator(Prisoner.objects.filter(prisoner_id__contains=search_term), 25)
    page = request.GET.get('page')
    try:
        prisoners = paginator.page(page)
    except PageNotAnInteger:
        prisoners = paginator.page(1)
    except EmptyPage:
        prisoners = paginator.page(paginator.num_page)
    return render(request,
                  "prisoner_list.html",
                  {'object_list': prisoners,
                   'term':search_term,
                   'page_obj':prisoners})


def query(request):
    if ('term' not in request.GET):
        return None
    term = filter(str.isalnum, str(request.GET['term']))
    return HttpResponse(
        serializers.serialize('json',Prisoner.objects.filter(
                prisoner_id__contains=request.GET['term']),
                              fields=('name','prisoner_id_raw', 'prisoner_id')))


class PrisonerList(ListView):
    template_name='prisoner_list.html'
    model=Prisoner
    paginate_by=10


class PrisonerDetail(DetailView):
    template_name="prisoner_detail.html"
    model=Prisoner


class PrisonerIndex(TemplateView):
    template_name="prisoner_index.html"
