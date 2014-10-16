from django.shortcuts import render
from django.http import HttpResponse

from PrisonerExpress.models import Program
from django.shortcuts import get_object_or_404, render, redirect

def index(request):
    total = len(Program.objects.all())
    return HttpResponse("There are %s programs" % total)

def details(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    return HttpResponse("Here are the details for prison %s" % program)

def create(request):
    if request.method == 'POST':
        new_program_id = create_program(request.POST['program_name'],
                                        request.POST['program_description'])
        return redirect('program_details', program_id=new_program_id)
    return render(request, "create_program.html")

def create_program(program_name,program_description="N/A"):
    if program_name is None :
        raise Http404
    p = Program( name=program_name,description = program_description)
    p.save()
    return p.id       

def edit(request):
    return HttpResponse("hello world");

 

