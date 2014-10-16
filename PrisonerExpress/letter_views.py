from django.shortcuts import render
from django.http import HttpResponse
from PrisonerExpress.models import Prisoner, Program


def new(request):
    context = {
        'prisoners':Prisoner.objects.all(),
        'programs':Program.objects.all()}
    if request.method == 'POST':
        if (request.POST['action'] == 'enroll'):
            context['results'] = enroll(request.POST['prisoner'], request.POST['program'])
        else:
            context['results'] = unenroll(request.POST['prisoner'], request.POST['program'])
    return render(request, "new_letter.html", context)        

def enroll(prisoner_id, program_id):
    prisoner = Prisoner.objects.get(pk=prisoner_id)
    program = Program.objects.get(pk=program_id)
    prisoner.programs.add(program)
    prisoner.save()
    return "%s was successfully enrolled in %s" % (prisoner.name, program.name)

    

def unenroll(prisoner_id, program_id):
    try:
        prisoner = Prisoner.objects.get(pk=prisoner_id)
        program = Program.objects.get(pk=program_id)
        prisoner.programs.remove(program)
        prisoner.save()
        return "%s was successfully unenrolled from %s" % (prisoner.name, program.name)
    except:
        return "An error has occurred, likely because either the prisoner or program are not valid, or the database is down."
