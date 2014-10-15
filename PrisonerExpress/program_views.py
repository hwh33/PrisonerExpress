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
    return HttpResponse("hello world");

def create_program(request):
    return HttpResponse("hello world");

def edit(request):
    return HttpResponse("hello world");

 

