from django.shortcuts import render, get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from PrisonerExpress.models import Program,Prisoner, IterationForm, Iteration
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PrisonerExpress.labels import Sheet, Specification, InvalidDimension
import os.path
from reportlab.graphics import shapes, renderPDF
from reportlab.pdfgen import canvas
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from reportlab.pdfbase.pdfmetrics import  stringWidth

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
                                        request.POST.get('active', False),
                                        request.POST.get('print_rule', False))
        return redirect('program_details', new_program_id)
    return render(request, "create_program.html")

def create_program(program_name,program_description="N/A", continuous=False, active=True,print_rule=False):
    if program_name is None :
        raise Http404
    p = Program( name=program_name,
                 description = program_description,
                 continuous=continuous,
                 active=active,
                 print_rule=print_rule)
    p.save()
    return p.id    


def edit(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST' and 'btn_edit' in request.POST:
        if program is None: 
            raise Http404
        program.name = request.POST['program_name']
        program.print_rule = request.POST.get('print_rule', False)
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
    

def mail(request, program_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=mailing_label.pdf'
    program = get_object_or_404(Program, id=program_id)
    """
        Required parameters
        -------------------
        sheet_width, sheet_height: positive dimension
            The size of the sheet.

        columns, rows: positive integer
            The number of labels on the sheet.

        label_width, label_size: positive dimension
            The size of each label.

        Margins and gaps
        ----------------
        left_margin: positive dimension
            The gap between the left edge of the sheet and the first column.
        column_gap: positive dimension
            The internal gap between columns.
        right_margin: positive dimension
            The gap between the right edge of the sheet and the last column.
        top_margin: positive dimension
            The gap between the top edge of the sheet and the first row.
        row_gap: positive dimension
            The internal gap between rows.
        bottom_margin: positive dimension
            The gap between the bottom edge of the sheet and the last row.

        Additional dimensions
        ---------------------
        corner_radius: positive dimension, default 0
            Gives the labels rounded corners with the given radius.

        Raises
        ------
        InvalidDimension
            If any given dimension is invalid (i.e., the labels cannot fit on
            the sheet).

    """
    _paper_width = 215.9
    _paper_height = 279.4
    _num_columns = 3
    _num_rows = 10
    _label_width = 66.675
    _label_height = 25.4 
    _top_margin = 12.7
    _bottom_margin = 12.7
    _left_margin = 5.5
    _right_margin = 5.5
    _row_gap = 0
    _column_gap = 0

    two_col_specs = Specification(215.9, 279.4, 2, 5, 102.3, 52.5, corner_radius=0.5, column_gap=5.9, row_gap=0)
    three_col_specs = Specification(215.9, 279.4, 3, 10, 66.675, 25.4, corner_radius=2,top_margin=12.7,row_gap=0,left_margin=5,right_margin=5)
    specs_dict = {"two_col_labels" : two_col_specs, "three_col_labels" : three_col_specs}
    def mailing_label(label, width, height, data):
            font="Helvetica"
            lines=[];
            num_lines=0;
            lines.append (data.name+", "+data.prisoner_id_raw) 
            num_lines += 1;
            if len(data.address.address_1)>0 :
                lines.append(data.address.address_1)
                num_lines += 1;
            if len(data.address.address_2)>0 :
                lines.append(data.address.address_2)
                num_lines += 1;
            if len(data.address.address_3)>0 :
                lines.append(data.address.address_3)
                num_lines += 1;
            lines.append(data.address.city+', '+data.address.state+', '+data.address.postal_code)
            num_lines += 1;
            fontsize=20;
            maxIndex=0;
            for i in range(1,num_lines):
                # calculate size of font 
                if len(lines[i])>len(lines[maxIndex]):
                    maxIndex=i
            fontsize=15
            add_width = stringWidth(lines[maxIndex], font, fontsize)
            text_width = width-10;
            font_height = 15
            while add_width > text_width:
                fontsize *= 0.9
                add_width = stringWidth(lines[maxIndex], font, fontsize)

            for i in range(0,num_lines):
                label.add(shapes.String(5, height-15-fontsize*i, lines[i],
                                    fontName=font, fontSize=fontsize))
            if program.print_rule :
                label.add(shapes.String(187,3, data.rules,
                                    fontName=font, fontSize=fontsize,textAnchor='end'))

    end_of_url_path = request.path.split('/')[-1]
    specs = specs_dict[end_of_url_path]
    sheet = Sheet(specs, mailing_label, border=True)
   
    for prisoner in program.prisoners.all():
        sheet.add_label(prisoner)
    
    p = canvas.Canvas(response,pagesize=sheet._pagesize)
    for page in sheet._pages:
            renderPDF.draw(page, p, 0, 0)
            p.showPage()
    p.save()
    return response;
    

def create_iteration(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    if request.method == 'GET':
        return render(request, "iteration_create.html", {"program":program, 'form':IterationForm()})
    form = IterationForm(request.POST)
    if (form.is_valid()):
        new_i = Iteration(name=form.cleaned_data['name'],
                          description=form.cleaned_data['description'],
                          parent=program)
        if program.continuous:
            current_iter = new_i.parent.get_current_iteration()
            print "Current iter: %s" %current_iter
            new_i.save()
            if current_iter != None:
                for prisoner in current_iter.prisoners.all():
                    if prisoner.active:
                        new_i.prisoners.add(prisoner)
                new_i.save()
        else:
            new_i.save()
        return redirect('iteration_details', iteration_id=new_i.id)
    return render(request,
                  'iteration_create.html',
                  {'form':IterationForm(),
                   'msg':'Form invalid!',
                   'program':program})


def input(request, program_id): 
    context = {"url":"/media/Letters/magic.png"}
    return  render(request,"letter_input.html",context)
    
class ProgramDetails(DetailView):
    model=Program
    template_name="program_detail.html"

class ProgramIndex(TemplateView):
    template_name="program_index.html"



def get_iteration_details(request, iteration_id):
    iteration = get_object_or_404(Iteration, pk=iteration_id)
    parts = iteration.prisoners.all()
    paginator = Paginator(parts, 25)
    
    page = 0
    if 'page' in request.GET:
        page = request.GET.get('page')
    try:
        ppl = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ppl = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ppl = paginator.page(paginator.num_pages)
    return render(request, 'iteration_detail.html', {'object':iteration,
                                            'object_list':ppl,
                                            'page_obj':paginator})
