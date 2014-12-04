from django.shortcuts import render
from django.http import HttpResponse
from PrisonerExpress.models import Prisoner, Program, ImageUploadForm, Letter
from django.contrib.auth.decorators import login_required


def public_page(request):
    context = {}
    return render(request,"index.html",context)
