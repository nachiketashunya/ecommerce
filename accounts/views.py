import random 
import string 

from django import forms
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import is_safe_url
from django.contrib import messages 
from django.views.generic import FormView 
from django.views import View
from django.http import HttpResponse

from .models import UserProfile, GuestEmail 
from .forms import UserProfileForm, LoginForm, GuestForm , UpdatePasswordForm



# Create your views here.
# View function takes a HttpRequest & returns HttpResponse 


def register_user(request):
	userprofileform = UserProfileForm(request.POST or None, label_suffix = " :") # label_suffix customizes label 

	if request.method == "POST":   # this checks the request methods 
		userprofileform = UserProfileForm(request.POST , request.FILES)  # request.FILES --- for file upload 

		if userprofileform.is_valid():  # Returns a Boolean Value
			try:
				userprofileform.save()
				messages.success(request, "You are successfully registered")
				
				return redirect("/login")

			except:
				return redirect('../registration')

	context = { 'forms' : userprofileform }  # key will be used in template 


	return render( request, 'accounts/register_user.html', context)  


def login(request):
	loginform = LoginForm( request.POST or None  , label_suffix = "" , auto_id = 'id_for_%s')  #inititalising form 
	next_ = request.GET.get('next') # getting next_url 
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None 
	
	print(request)


	if request.method == "POST":
		if loginform.is_valid():
			username = loginform.cleaned_data.get('username')  #this username should be similar to form's field
			password = loginform.cleaned_data.get('password')  #this password should be similar to form's field
			

			try:
				user = UserProfile.objects.get( email = username , password = password )  #getting object of matched user
				print("username set ")
				request.session['username'] = username  #assigning username to request session
				#request.session.set_expiry(30)  #This can be set to expires the session 
				
			except:
				messages.warning(request , "Password is incorrect")
				return redirect('/login')

			if user is not None:
				try:
					del request.session['guest_email_id']
					del request.session['guest_email']
				except:
					pass 

				if is_safe_url(redirect_path, request.get_host()):
					return redirect(redirect_path)
				else:
					return redirect('/productpage')


	context = { 'form': loginform, 
				'title' : 'login'
			}


	return render( request, 'accounts/login.html' , context)

def dashboard(request):
	return render( request, 'accounts/dashboard.html')

def logout(request):
	for key in list(request.session.keys()):
		del request.session[key]

	return redirect('/login')

#view for register guest user
def guest_register(request):
	guest_form = GuestForm(request.POST or None)
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None 

	if request.method == "POST":
		if guest_form.is_valid():
			email = guest_form.cleaned_data.get('username')
			new_guest_email = GuestEmail.objects.create(email = email)
			request.session['guest_email_id'] = new_guest_email.id 

			request.session['guest_email'] = email

			if is_safe_url(redirect_path, request.get_host()):  #checking path is safe or not ?
				return redirect(redirect_path)
			else:
				return redirect('/registration')

	return redirect('/registration')


def update_password(request):
	if 'username' in request.session:
		form = UpdatePasswordForm(request.POST or None)
		user = UserProfile.objects.get( email = request.session['username'])

		if request.method == "POST":
			if form.is_valid():
				current_password = form.cleaned_data.get('current_password')
				new_password = form.cleaned_data.get('new_password')
				confirm_new_password = form.cleaned_data.get('confirm_new_password')

				try:
					if current_password == user.password:
						if new_password == confirm_new_password:
							print(user.password)
							UserProfile.objects.filter(email =  request.session['username']).update(password = new_password , 
																						confirm_password = confirm_new_password)  #using update function to update details 

							return redirect('/profile')
						else:
							raise forms.ValidationError("Password didn\'t match")

					else:
						raise forms.ValidationError("Password didn\'t match")

				except:
					raise forms.ValidationError("Please enter valid password")

		context = { 
					'form' : form ,
					'title' : 'Update Password'
				}

		return render(request, 'accounts/update.html' , context)

	else:
		return redirect("/login")

