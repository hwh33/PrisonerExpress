from django.shortcuts import render, get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from PrisonerExpress.models import Program,Prisoner
import labels
import os.path
from reportlab.graphics import shapes, renderPDF
from reportlab.pdfgen import canvas
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def index(request):
    program_list = Program.objects.all()
    context = {'program_list':program_list}
    return render(request,"program_list.html",context)

def details(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    context = {'program':program}
    return render(request,"detail_program.html",context)

@login_required
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

@login_required
def edit(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST' and 'btn_edit' in request.POST:
        if program is None: 
            raise Http404
        program.name = request.POST['program_name']
        program.description = request.POST['program_description']
        program.save();
        return redirect('program_details', program.id)
    if request.method == 'POST' and 'btn_add' in request.POST:
        prisoner = None
        prisoner_id = request.POST['prisoner']
        if not prisoner_id == -1:
            prisoner = Prisoner.objects.get(pk=prisoner_id)
        program.prisoners.add(prisoner)
        program.save();
        return redirect('program_details', program.id)
    context = {'program':program,'prisoner_list':Prisoner.objects.all()}
    return  render(request,"edit_program.html",context)
    
@login_required
def mail(request, program_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=mailing_label.pdf'
    specs = labels.Specification(210, 297, 2, 6, 90, 48, corner_radius=2)
    
    def mailing_label(label, width, height, data):
            
            label.add(shapes.String(5, height-20, data.name,
                                    fontName="Helvetica", fontSize=20))
            h=1;
            if len(data.address.address_1)>0 :
                label.add(shapes.String(5, height-h*30-20, data.address.address_1,
                                            fontName="Helvetica", fontSize=15))
                h=h+1;
            if len(data.address.address_2)>0 :
                label.add(shapes.String(5, height-h*30-20, data.address.address_2,
                                        fontName="Helvetica", fontSize=15))
                h=h+1;
            if len(data.address.address_3)>0 :
                label.add(shapes.String(5, height-h*30-20, data.address.address_3,
                                        fontName="Helvetica", fontSize=15))
                h=h+1;
            label.add(shapes.String(5, height-h*30-20, data.address.city+', '+data.address.state+', '+data.address.postal_code,
                                    fontName="Helvetica", fontSize=15)) 

    sheet = labels.Sheet(specs, mailing_label, border=True)
    program = get_object_or_404(Program, id=program_id)
    for prisoner in program.prisoners.all():
        sheet.add_label(prisoner)
    
    p = canvas.Canvas(response,pagesize=sheet._pagesize)
    for page in sheet._pages:
            renderPDF.draw(page, p, 0, 0)
            p.showPage()
    p.save()
    return response;

@login_required
def input(request, program_id): 
    context = {"url":"/media/Letters/magic.png"}
    return  render(request,"letter_input.html",context)
    
class ProgramDetails(DetailView):
    model=Program
    template_name="program_detail.html"

class ProgramIndex(TemplateView):
    template_name="program_index.html"
