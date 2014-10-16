from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from PrisonerExpress.models import Program
from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    program_list = Program.objects.all()
    context = {'program_list':program_list}
    return render(request,"program_list.html",context)

def details(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    context = {'program':program}
    return render(request,"detail_program.html",context)

def create(request):
    if request.method == 'POST':
        new_program_id = create_program(request.POST['program_name'],
                                        request.POST['program_description'],
                                        request.POST.get('continuous', False),
                                        request.POST.get('active', False))
        return redirect('program_details', new_program_id)
    return render(request, "create_program.html")

def create_program(program_name,program_description="N/A", continuous=False, active=True):
    if program_name is None :
        raise Http404
    p = Program( name=program_name,
                 description = program_description,
                 continuous=continuous,
                 active=active)
    p.save()
    return p.id         

def edit(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST':
        if program is None: 
            raise Http404
        program.name = request.POST['program_name']
        program.description = request.POST['program_description']
        program.save();
        return redirect('program_details', program_id=program.id)
    context = {'program':program}
    return  render(request,"edit_program.html",context)


class ProgramDetails(DetailView):
    model=Program
    template_name="program_detail.html"

class ProgramIndex(TemplateView):
    template_name="program_index.html"
