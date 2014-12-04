from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from PrisonerExpress.models import UserProfile,UserProfileForm
from PrisonerExpress.forms import UserCreateForm
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

def user_ctrl(request):
	cur_user=request.user
	msg=None
	if cur_user.is_superuser==True :
		users = User.objects.filter( Q(is_superuser=False) )
	elif cur_user.is_staff == True:
		users = User.objects.filter( Q(is_superuser=False),Q(is_staff=False))
	else:
		msg="No permission"

	if request.method == 'POST':
		username = request.POST['username']
		pem_lv = request.POST['level']
		user = User.objects.get(username=username)
		if pem_lv == "admin":
			user.is_staff=True
		elif pem_lv == "volunteer":
			user.is_staff=False
			user.profile.is_volunteer=True
		elif pem_lv == "public_user":
			user.is_staff=False
			user.profile.is_volunteer=False
		print user.is_staff, user.profile.is_volunteer
		user.profile.save()
		user.save()
		message="Change permission successfully"
		return render(request,'user_ctrl.html',{'users':users,'message':message})
	return render(request,'user_ctrl.html',{'users':users,'message':msg})

def user_profile(request):
	render_to_response('user_ctrl.html',dict(userctrlform=uf),context_instance=RequestContext(request))
	
def user_register(request):
	uf = UserCreateForm(request.POST or None,prefix='user')
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
	return render(request,'user_register.html',	dict(userform=uf,
                                              	userprofileform=upf),
                                               )


