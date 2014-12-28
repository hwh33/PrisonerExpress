from django.shortcuts import render
from django.http import HttpResponse
from PrisonerExpress.models import Prisoner, Program, ImageUploadForm, Letter, Subprogram
from django.contrib.auth.decorators import login_required


def index(request):
    letters = Letter.objects.all()
    context = {'letters':letters}
    return render(request,"letter_list.html",context)

def edit(request,letter_id):
    letter=Letter.objects.get(pk=letter_id)
    context = {'letter':letter}
    if request.method == 'POST':
        letter.content = request.POST['content']
        letter.save()
        context['message']="save successfully"
    return render(request,"edit_letter.html",context)

def new(request):
    programs = Program.objects.all()
    current_iters = {}
    for p in programs:
        c = p.get_current_iteration()
        if c is not None:
            sub_programs = c.subprogram_set.all()
            current_iters[p] = sub_programs

    print current_iters
    context = { 'data': current_iters }
    
    if request.method == 'POST':
        if (request.POST['action'] == 'enroll'):
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                context['message'] = enroll(request.POST['prisoner'], request.POST['programs'], form.cleaned_data['image'])
            else:
                context['message'] = enroll(request.POST['prisoner'], request.POST['programs'])
        else:
            context['message'] = unenroll(request.POST['prisoner'], request.POST['programs'])

    return render(request, "new_letter.html", context)        


def enroll(prisoner_id, program_ids,letter_img=None):
    prisoner = Prisoner.objects.get(pk=prisoner_id)
    for program_id in program_ids:
        subprogram = Subprogram.objects.get(pk=program_id)
        prisoner.programs.add(subprogram)
        if letter_img :
            letter = Letter(prisoner = prisoner, program = program, image = letter_img)
            letter.save()
        prisoner.save()
    return "%s was successfully enrolled" % prisoner.name

    

def unenroll(prisoner_id, program_ids):
    try:
        prisoner = Prisoner.objects.get(pk=prisoner_id)
        for program_id in program_ids:
            program = Subprogram.objects.get(pk=program_id)
            prisoner.programs.remove(program)
            prisoner.save()
        return "%s was successfully unenrolled"
    except:
        return "An error has occurred, likely because either the prisoner or program are not valid, or the database is down."
