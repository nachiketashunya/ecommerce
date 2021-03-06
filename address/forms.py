from django import forms
from .models import Address


# AddressForm to create address for shipping and billing
class AddressForm(forms.ModelForm):
	class Meta:
		fields = '__all__'
		model = Address
		exclude = [ 'billing_profile', 'address_type']  #these fields won't be included in ModelForm


		widgets = {
					'address_line_1' : forms.TextInput(attrs = { 'class':'form-control'}),
					'address_line_2' : forms.TextInput(attrs = { 'class':'form-control'}),
					'city' : forms.TextInput(attrs = {'class':'form-control'}),
					'pincode':forms.TextInput(attrs = {'class':'form-control'}),
					'state' : forms.TextInput(attrs = {'class':'form-control'}),
					'country': forms.TextInput(attrs = {'class' : 'form-control' , 'readonly':'readonly'})
				}
