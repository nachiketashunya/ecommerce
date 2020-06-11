from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from .models import BillingProfile , Card
from django.utils.http import is_safe_url
import stripe
# Create your views here.

#Stripe is a payment gateway so it must be understood firmly

stripe.api_key = "sk_test_bOISPZLKdLIDyhcipROLQoqD004hS82SKc"

STRIPE_PUBLISH_KEY = "pk_test_SP0uaJPtuBkFrHqFWhMpWdzL00eb0skLUz"

def payment_method(request):
	if 'username' in request.session or 'guest_email_id' in request.session:
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		my_customer_id = billing_profile.customer_id 	#fetching customer_id from billing profile model

	if not billing_profile:
		return redirect('cart/home')

	STRIPE_PUBLISH_KEY = "pk_test_SP0uaJPtuBkFrHqFWhMpWdzL00eb0skLUz"

	next_url = None
	next_  = request.GET.get("next")

	if is_safe_url(next_ , request.get_host()):
		next_url = next_

	context = {
				"publish_key" : STRIPE_PUBLISH_KEY ,
				"next_url" : next_url
			}

	return render(request, 'billing/payment_method.html', context)

#This view function stores the card info in database
def payment_method_create(request):
	if request.method == "POST":
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

		if not billing_profile:
			return HttpResponse( { "message" : "Cannot find this user"}, status_code = 401)

		token = request.POST.get('stripeToken') 	#stripe generates a token to enhance high security
		next_url = request.POST.get('next_url')

		if token is not None:
			new_card_obj = Card.objects.add_new(billing_profile , token)	#New card object is created

		return redirect('/cart/checkout')

	return HttpResponse("error", status_code = 401)
