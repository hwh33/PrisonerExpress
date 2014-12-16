from django.shortcuts import render, redirect
from django.template import Context, RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from PrisonerExpress.models import UserProfile,UserProfileForm, UserRegisterCode
from PrisonerExpress.forms import UserCreateForm
from django.contrib.auth.models import  User
from django.db.models import Q
from django.conf import settings
import uuid,datetime


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
				return redirect('index')

	return render(request,'user_login.html')


def user_logout(request):
	logout(request)
	return redirect('index')

def user_ctrl(request,):

	if request.method == 'POST':
		username = request.POST['username']
		pem_lv = request.POST['level']
		user = User.objects.get(username=username)
		msg=None
		if pem_lv == "admin":
			user.is_staff=True
			user.profile.save()
			user.save()
			msg="Change permission successfully"
		elif pem_lv == "volunteer":
			user.is_staff=False
			user.profile.save()
			user.save()
			msg="Change permission successfully"
		elif pem_lv == "cancel":
			user.profile.delete()
			user.delete()
			msg="Cancel account successfully"
		return redirect('user_ctrl')
	today=datetime.datetime.now()

	if (settings.REGISTER_CODE =='' or (today-settings.REGISTER_TIME).days>7):
		settings.REGISTER_TIME=datetime.datetime.now()
		settings.REGISTER_CODE=str(uuid.uuid4())
	register_code = settings.REGISTER_CODE
	cur_user=request.user
	msg=None
	if cur_user.is_superuser==True :
		users = User.objects.filter( Q(is_superuser=False) )
	elif cur_user.is_staff == True:
		users = User.objects.filter( Q(is_superuser=False),Q(is_staff=False))
	else:
		msg="No permission"
	return render(request,'user_ctrl.html',{'users':users,'message':msg,'reg_code':register_code})


def user_register(request):
	uf = UserCreateForm(request.POST or None,prefix='user')
	upf = UserProfileForm(request.POST or None,prefix='userprofile')
	message=None;
	if request.method == 'POST':
		uf = UserCreationForm(request.POST, prefix='user')
       	upf = UserProfileForm(request.POST, prefix='userprofile')
        if uf.is_valid() * upf.is_valid():
        	register_code = upf.cleaned_data['register_code']

        	if(register_code==settings.REGISTER_CODE):
	            user = uf.save()
	            userprofile = upf.save(commit=False)
	            userprofile.user = user
	            userprofile.save()
	            user.save()
	            return redirect('user_login')
	        else:
	        	return render(request,'user_register.html',	{'userform':uf,
                                              	'userprofileform':upf,'message':'ask staff for register code'}
                                              	)

	return render(request,'user_register.html',	{'userform':uf,
                                              	'userprofileform':upf,'message':message}
                                              	)
def user_profile(request):
	user= request.user
	return render(request,'user_profile.html')

def user_edit(request):
	if request.method == 'POST' and 'btn_edit' in request.POST:
		user=request.user
		if user is None:
			raise Http404
		user.profile.phone_number = request.POST['user_number']
		user.profile.gender = request.POST['sex']
		user.profile.save()
		return redirect('user_profile')
	return render(request,'edit_user.html')

