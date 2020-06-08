from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address 
from billing.models import BillingProfile 
from cart.models import Cart 
from order.models import Order 
from django.utils.http import is_safe_url 

# Create your views here.

def checkout_address(request):
	addressform = AddressForm(request.POST or None )
	next_url = request.GET.get('next')
	next_post = request.POST.get('next')

	redirect_path = next_url or next_post or None

	if request.method == "POST":
		if addressform.is_valid():
			instance = addressform.save( commit = False ) # We don't want to save instance at this time 
			billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

			if billing_profile is not None:
				address_type = request.POST.get('address_type', 'shipping') # This is same as checkout.html 
				instance.billing_profile = billing_profile
				instance.address_type = address_type
				instance.save()

				request.session[address_type+ '_address_id'] = instance.id # Assigning address_id to request.session
			
			else:
				return redirect('/cart/checkout')

			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect('/cart/checkout') 


	return redirect('/cart/checkout')

def checkout_address_reuse(request):
	if 'username' in request.session or 'guest_email_id' in request.session:

		next_ = request.POST.get('next')
		next_url = request.GET.get('next')
		redirect_path = next_ or next_url or None

		cart_obj , cart_obj_created = Cart.objects.new_or_get(request) # Getting cart object to extract order object 

		if request.method == "POST":
			shipping_address = request.POST.get('shipping_address' , None) # Name of radio button 
			address_type = request.POST.get('address_type', 'shipping_address') # Same as in checkout.html 

			billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)

			order_obj,order_obj_created = Order.objects.new_or_get(billing_profile = billing_profile,cart_obj = cart_obj)

			if shipping_address is not None:
				qs = Address.objects.filter( billing_profile = billing_profile, id = shipping_address)

				if qs.exists():
					request.session[ address_type + '_id'] = shipping_address 


					if address_type == 'shipping_address':
						order_obj.shipping_address = Address.objects.get( id = shipping_address)

					if address_type == 'billing_address':
						order_obj.billing_address = Address.objects.get( id = shipping_address)

					order_obj.save()

				if is_safe_url(redirect_path , request.get_host()):
					return redirect(redirect_path)
				else:
					return redirect('/cart/checkout')

	return redirect('/cart/checkout/')


