from django.db import models
from accounts.models import UserProfile, GuestEmail
from django.db.models.signals import post_save, pre_save
import stripe 

stripe.api_key = 'sk_test_bOISPZLKdLIDyhcipROLQoqD004hS82SKc'
# Create your models here.

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




class BillingProfile(models.Model):
	user = models.OneToOneField(UserProfile, null = True,blank = True,on_delete = models.CASCADE)
	email = models.EmailField()
	active = models.BooleanField(default = True )
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = BillingProfileManager()

	def __str__(self):
		return self.email 

	customer_id = models.CharField(max_length = 120 , null = True, blank = True)

	def get_cards(self):
		cards = Card.objects.filter( billing_profile = self)
		return cards 

	def has_card(self):
		card_qs = self.get_cards()

		return card_qs.exists()

	def default_card(self):
		default_cards = self.get_cards().filter( active = True, default = True)

		if default_cards.exists():
			return default_cards.first()

	def set_cards_inactive(self):
		cards_qs = self.get_cards()
		cards_qs.update( active = False)

		return cards_qs.filter( active = True).count()

def billing_profile_created_reciever(sender, instance, *args, **kwargs):
	if not instance.customer_id and instance.email:
		print("ACTUAL API REQUEST send to stripe/braintree")

		customer = stripe.Customer.create(email = instance.email)
		print(customer)

		instance.customer_id = customer.id 

		print(customer.id)

pre_save.connect(billing_profile_created_reciever , sender = BillingProfile)



def user_created_reciever(sender , instance , created , *args , **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user = instance, email = instance.email)

post_save.connect(user_created_reciever , sender = UserProfile)


class CardManager(models.Manager):
	def all(self, *args, **kwargs): # ModelKlass.objects.all() --> ModelKlass.objects.filter(active = True)
		return self.get_queryset().filter(active = True)

	def add_new(self, billing_profile , token):
		if token:
			print("token recieved in billing_profile")
			customer = stripe.Customer.retrieve(billing_profile.customer_id)
			stripe_card_response = stripe.Customer.create_source(customer.id , source = token)
			print(customer)
			print("gapee")
			print(stripe_card_response)

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


class Card(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete = models.CASCADE)
	stripe_id = models.CharField(max_length = 120)
	brand = models.CharField(max_length = 120 , null = True , blank = True)
	country = models.CharField(max_length = 120 , null = True , blank = True)
	exp_month = models.IntegerField(null = True , blank = True)
	exp_year = models.IntegerField(null = True, blank = True)
	last4 = models.CharField(max_length = 4 , null = True, blank = True)
	default = models.BooleanField(default = True)
	active = models.BooleanField(default = True)
	timestamp = models.DateTimeField(auto_now_add = True)

	objects = CardManager()


	def __str__(self):
		return "{} {}".format(self.brand , self.last4)


def new_card_post_save_reciever(sender, instance , created , *args, **kwargs ):
	if instance.default:
		billing_profile = instance.billing_profile
		qs = Card.objects.filter(billing_profile = billing_profile).exclude( pk = instance.pk).update(default = False)

post_save.connect(new_card_post_save_reciever , sender = Card)