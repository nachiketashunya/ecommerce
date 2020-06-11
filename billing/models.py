from django.db import models
from accounts.models import UserProfile, GuestEmail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import stripe

stripe.api_key = 'sk_test_bOISPZLKdLIDyhcipROLQoqD004hS82SKc'
# Create your models here.


#Manager to control billing profiles
class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		user = None

		if 'username' in request.session:
			user = UserProfile.objects.get(email = request.session['username'])

		guest_email_id = request.session.get('guest_email_id')

		created = False
		obj = None

		if user is not None:
			obj , created = self.model.objects.get_or_create(user = user , email = user.email)

		elif guest_email_id is not None:
			guest_email_obj = GuestEmail.objects.get( id = guest_email_id )
			obj , created = self.model.objects.get_or_create(email = guest_email_obj.email)
		else:
			pass

		return obj , created


# ModelClass to store BillingProfile for order
class BillingProfile(models.Model):
	user = models.OneToOneField(UserProfile, null = True, blank = True, on_delete = models.CASCADE) #user is assigned to billing_profile
	email = models.EmailField()
	active = models.BooleanField(default = True )
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = BillingProfileManager() #Manager to control billing_profile

	def __str__(self):
		return self.email

	customer_id = models.CharField(max_length = 120 , null = True, blank = True)	#Customer id to make order

	def get_cards(self):	#view function to get all cards related to current billing_profile
		cards = Card.objects.filter( billing_profile = self)
		return cards

	def has_card(self): 	#check for saved cards
		card_qs = self.get_cards()

		return card_qs.exists()

	def default_card(self): 	#checking for default card for this billing_profile
		default_cards = self.get_cards().filter( active = True, default = True)

		if default_cards.exists():
			return default_cards.first()

	def set_cards_inactive(self): 	#deactive card for purchase
		cards_qs = self.get_cards()
		cards_qs.update( active = False)

		return cards_qs.filter( active = True).count()


#this receiver is executed before saving billing_profile object
# @receiver(pre_save, sender = BillingProfile)
def billing_profile_created_reciever(sender, instance, *args, **kwargs):
	if not instance.customer_id and instance.email:
		customer = stripe.Customer.create(email = instance.email)	#stripe is a payment gateway

		instance.customer_id = customer.id

pre_save.connect(billing_profile_created_reciever , sender = BillingProfile)


# this is receiver is executed after saving billing_profile to set user in billing_profile
# @receiver(post_save, sender = UserProfile)  << alternate way to connnect post_save signal
def user_created_reciever(sender , instance , created , *args , **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user = instance, email = instance.email)

post_save.connect(user_created_reciever , sender = UserProfile)


#manager to control card objects
class CardManager(models.Manager):
	def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active = True)
		return self.get_queryset().filter(active = True)

	def add_new(self, billing_profile , token):
		if token:	#When information is submitted js generates a token for security reasons
			customer = stripe.Customer.retrieve(billing_profile.customer_id)	#This fetches customer id
			stripe_card_response = stripe.Customer.create_source(customer.id, source = token)

			new_card = self.model(
								billing_profile = billing_profile,
								stripe_id = stripe_card_response.id,
								brand = stripe_card_response.brand ,
								country = stripe_card_response.country ,
								exp_month = stripe_card_response.exp_month ,
								exp_year = stripe_card_response.exp_year,
								last4 = stripe_card_response.last4
								)

			new_card.save()
			return new_card

		return None


#Card Model to store information about cards for payment
class Card(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete = models.CASCADE)	#Every card should have billing_profile
	stripe_id = models.CharField(max_length = 120)	#This paymet gateway
	brand = models.CharField(max_length = 120 , null = True , blank = True)
	country = models.CharField(max_length = 120 , null = True , blank = True)
	exp_month = models.IntegerField(null = True , blank = True)
	exp_year = models.IntegerField(null = True, blank = True)
	last4 = models.CharField(max_length = 4 , null = True, blank = True)	#last four digits of card number
	default = models.BooleanField(default = True)
	active = models.BooleanField(default = True)
	timestamp = models.DateTimeField(auto_now_add = True)

	objects = CardManager() 	#Manager to control card objects


	def __str__(self):
		return "{} {}".format(self.brand , self.last4)

# @receiver(post_save, sender = Card)
# This receiver is executed after saving card object
def new_card_post_save_reciever(sender, instance, created, *args, **kwargs ):
	if instance.default:
		billing_profile = instance.billing_profile
		qs = Card.objects.filter(billing_profile = billing_profile).exclude( pk = instance.pk).update(default = False)

post_save.connect(new_card_post_save_reciever, sender = Card)
