from django.shortcuts import render, redirect 
from .models import Cart, CartManager
from products.models import Product 
from django.http import HttpResponse
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile , Card 
from accounts.models import GuestEmail
from address.forms import AddressForm
from address.models import Address 
from order.models import Order 
# Create your views here.

def cart(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	#print(request.session.get('cart_id'))

	context = {'cart': cart_obj,
				'title' : 'Cart'}

	return render(request, 'cart/cart.html', context)


def cartupdate(request):
	product_id = request.POST.get('product_id')
	print(product_id)

	if product_id is not None:
		try:
			product_obj = Product.objects.get(id = product_id)

		except Product.DoesNotExist:
			print("This product doesn't exist")
			return redirect('/cart')

		cart_obj , new_obj = Cart.objects.new_or_get(request)

		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
		else:
			cart_obj.products.add(product_obj) 

		request.session['cart_items'] = cart_obj.products.count()


	return redirect('/cart')

def checkout(request):
	cart_obj , cart_created = Cart.objects.new_or_get(request)
	next_url = request.build_absolute_uri
	has_card = None

	order_obj = None 

	if cart_created or cart_obj.products.count() == 0:
		return redirect('/cart')

	loginform = LoginForm()
	guestform = GuestForm()
	billing_addressform = AddressForm()

	shipping_address_id = request.session.get('shipping_address_id', None)
	billing_address_id = request.session.get('billing_address_id' , None)

	address_qs = None

	billing_profile , billing_profile_created = BillingProfile.objects.new_or_get(request)

	if billing_profile is not None:
		if 'username' in request.session or 'guest_email_id' in request.session:
			address_qs = Address.objects.filter( billing_profile = billing_profile)

		order_obj , order_obj_created = Order.objects.new_or_get(billing_profile , cart_obj)

		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id = shipping_address_id)
			del request.session['shipping_address_id']

		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id = billing_address_id)
			del request.session['billing_address_id']

		if billing_address_id or shipping_address_id:
			order_obj.save()

		has_card = billing_profile.has_card()

		if request.method == "POST":
			is_done = order_obj.check_done()
			if is_done:
				order_obj.mark_paid()
				request.session['cart_items'] = 0
				del request.session['cart_id']
				return redirect('/cart/successful')


	context = { 'loginform' : loginform , 
				'guestform' : guestform ,
				'billing_profile': billing_profile,
				'next_url' : next_url,
				'addressform' : billing_addressform,
				'address_type': 'shipping' ,
				'address_qs' : address_qs,
				'object' : order_obj,
				'has_card': has_card,
				'cart' : cart_obj
			}

	return render(request, 'cart/checkout.html' , context)

def successful(request):
	return render(request, 'cart/successful.html' )


