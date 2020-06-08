from django import forms
from .models import Review 

#RevieForm shows user a form so that they can review product 
class ReviewForm(forms.Form):
	reviewed_by = forms.EmailField( widget = forms.EmailInput(attrs = { 
																		    'class' : 'form-control', 
																			'readonly' : 'readonly', 
																			'required' : 'required', 
																			'placeholder' : 'Enter Email'
																		}))


	product_id = forms.CharField(widget = forms.TextInput(attrs = {		
																		'class' : 'form-control', 
																		'type' : 'hidden', 
																		'required' : 'required',
																		'readonly' : 'readonly'
																	}))
	

	description = forms.CharField(widget = forms.Textarea( attrs = {	
																		'class' : 'form-control', 	
																		'placeholder' : 'Write review'
																	}))
