from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from .models import BillingProfile , Card
from django.utils.http import is_safe_url
import stripe 
# Create your views here.


stripe.api_key = "sk_test_bOISPZLKdLIDyhcipROLQoqD004hS82SKc"

STRIPE_PUBLISH_KEY = "pk_test_SP0uaJPtuBkFrHqFWhMpWdzL00eb0skLUz"

def payment_method(request):
	if 'username' in request.session or 'guest_email_id' in request.session:
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		my_customer_id = billing_profile.customer_id 
		print(my_customer_id)

	if not billing_profile:
		return redirect('cart/home')

	print("Payment Mehtod")

	STRIPE_PUBLISH_KEY = "pk_test_SP0uaJPtuBkFrHqFWhMpWdzL00eb0skLUz"

	next_url = None
	next_  = request.GET.get("next")

	if is_safe_url(next_ , request.get_host()):
		print("Reached")
		next_url = next_
		print(next_url)

	context = { "publish_key" : STRIPE_PUBLISH_KEY , 
				"next_url" : next_url 
			}

	return render(request, 'billing/payment_method.html', context)

def payment_method_create(request):
	if request.method == "POST":
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if not billing_profile:
			return HttpResponse( { "message" : "Cannot find this user"}, status_code = 401)

		token = request.POST.get('stripeToken')
		next_url = request.POST.get('next_url')

		print("Payment Method Create")

		if token is not None:
			print("token is got")
			new_card_obj = Card.objects.add_new(billing_profile , token)
			print("new card is added")

		return redirect('/cart/checkout')

	return HttpResponse("error" , status_code = 401)