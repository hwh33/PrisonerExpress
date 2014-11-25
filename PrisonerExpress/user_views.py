from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from PrisonerExpress.models import UserProfile,UserProfileForm
from django.contrib.auth.models import Group, User 
from django.db.models import Q

# Create your views here.
def user_login(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
	return render(request,'user_login.html')


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

#admin required
def user_ctrl(request):

	users = User.objects.filter( Q(is_superuser=False) )
	msg = None
	if request.method == 'POST':
		username = request.POST['username']
		groupname = request.POST['groupname']
		print groupname 
		group = Group.objects.get(name=groupname)
		user = User.objects.get(username=username)
		group.user_set.add(user)
		group.save()
		user.save()
		result="succ"
		return render_to_response('user_ctrl.html',{'users':users,'result':result},context_instance=RequestContext(request))
	return render_to_response('user_ctrl.html',{'users':users},context_instance=RequestContext(request))

def user_profile(request):
	render_to_response('user_ctrl.html',dict(userctrlform=uf),context_instance=RequestContext(request))
	
def user_register(request):
	uf = UserCreationForm(request.POST or None,prefix='user')
	upf = UserProfileForm(request.POST or None,prefix='userprofile')
	if request.method == 'POST':
		uf = UserCreationForm(request.POST, prefix='user')
       	upf = UserProfileForm(request.POST, prefix='userprofile')
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.user = user
            userprofile.save()
            return redirect('user_login')
	return render_to_response('user_register.html',	dict(userform=uf,
                                              	userprofileform=upf),
                                               	context_instance=RequestContext(request))


