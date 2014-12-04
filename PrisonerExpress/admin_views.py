from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from PrisonerExpress.models import Prison, Prisoner, PrisonerForm
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.contrib.auth.decorators import login_required

def settings(request):
    return render(request,"admin_settings.html", {})
