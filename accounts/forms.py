from django import forms 
from .models import UserProfile 
from django.utils.translation import gettext_lazy as _


class UserProfileForm(forms.ModelForm):  #this is ModelForm
	class Meta:
		model  = UserProfile
		fields = '__all__'

		labels = { 'password' : _('Your Password')} #This is used to customized labels in ModelForm

		# widget is used to customize the view of fields 
		widgets = { 
			'name' : forms.TextInput(attrs= {'class': 'form-control'}),
			'email' : forms.TextInput(attrs= {'class': 'form-control'}),
			'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control'}),
			'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
			'gender': forms.Select(attrs={'class': 'form-control'}),
			'profile_image' : forms.ClearableFileInput(attrs = {'class' : 'form-control'}),

		}

	def clean_email(self):  # function name should contain field name ('email')
		email = self.cleaned_data.get('email')  # getting email from cleaned data 
		qs = UserProfile.objects.filter( email = email)   # getting queryset of matched email 

		if qs.exists():  # check whether queryset exists or not
			raise forms.ValidationError('email already exists')
		else:
			return email

	def clean_phone_no(self): # function name should contain field name ('phone_no')
		phone_number = self.cleaned_data.get('phone_no')
		qs = UserProfile.objects.filter(phone_no = phone_number)

		if qs.exists():
			raise forms.ValidationError('email already exists')
		else:
			return phone_number

	def clean(self):  # this is for password 
		data = self.cleaned_data
		password = self.cleaned_data.get("password")
		confirm_password = self.cleaned_data.get("confirm_password")

		if password == confirm_password: # matching both passwords 
			return data
		else:
			raise forms.ValidationError('password didn\'t match')



class LoginForm(forms.Form): 
	username = forms.CharField( widget = forms.TextInput( attrs = {'class':'form-control', 'placeholder':'Enter Username'} ))
	password = forms.CharField( widget = forms.PasswordInput(attrs = { 'class': 'form-control', 'placeholder': 'Enter Password'}))

class GuestForm(forms.Form):
	username = forms.EmailField( widget = forms.TextInput( attrs = {'class':'form-control', 'placeholder':'Enter Username'}))

class UpdatePasswordForm(forms.Form):
	current_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}))
	new_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}))
	confirm_new_password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'form-control'}))
