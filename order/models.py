from django.db import models
from billing.models import BillingProfile
from address.models import Address
from cart.models import Cart
from django.db.models.signals import pre_save , post_save
from ecommerce.utils import unique_order_id_generator
from decimal import Decimal
from django.dispatch import receiver

# Create your models here.
ORDER_STATUS_CHOICES = (('created', 'Created'), ('shipped', 'Shipped'), ('paid','Paid'), ('refunded', 'Refunded'))

#Manager to control order objects
class OrderManager(models.Manager): #inherits manager class to use Manager's method
	def new_or_get(self, billing_profile, cart_obj):
		created = False
		qs = self.get_queryset().filter(
										billing_profile = billing_profile ,
										cart = cart_obj ,
										active =  True  ,
										status = 'created')

		if qs.count() == 1:
			obj = qs.first()

		else:
			obj = self.model.objects.create(billing_profile = billing_profile , cart = cart_obj)
			created = True

		return obj , created


#ModelClass to save order_object in database
class Order(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete = models.CASCADE ,
														null = True,
														blank = True
										)	#Every order should contain billing profile

	shipping_address = models.ForeignKey(Address, 	related_name = 'shipping_address',
													on_delete = models.CASCADE,
													null = True ,
													blank = True
										)	#Every order should be delivered to an appropriate location

	billing_address = models.ForeignKey(Address,	related_name = 'billing_address',
													on_delete = models.CASCADE,
													null = True ,
													blank = True
										)	#Every bill has billing_address

	order_id = models.CharField(max_length = 120)	#order_id is necessary to track the record

	status = models.CharField(  default = 'created' ,
								max_length = 50,
								choices = ORDER_STATUS_CHOICES
							)

	cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
	shipping_total = models.DecimalField(default = 100.00 , decimal_places = 2 , max_digits = 100)
	total = models.DecimalField(default = 100.00 , decimal_places = 2 , max_digits = 100)
	active = models.BooleanField(default = True)
	objects = OrderManager()	#Manager to control order objects

	def update_total(self):	#Every time it updates the total price of all items
		cart_total = self.cart.total

		if self.cart.subtotal > 1000:
			self.shipping_total = 0.0
		else:
			self.shipping_total = 100.0

		new_total = cart_total +  Decimal(self.shipping_total)
		self.total = new_total
		self.save()

		return new_total

	def check_done(self):	#it checks for all information to initialise final checkout process
		billing_profile = self.billing_profile
		billing_address = self.billing_address
		shipping_address = self.shipping_address

		if billing_profile and shipping_address and billing_address and self.total > 0 :
			return True
		return False

	def mark_paid(self):	#This shows that money is paid
		if self.check_done():
			self.status = "paid"
		return self.status


# @receiver(pre_save, sender = Order) << alternate way to connect pre_save signal
#this receiver create order_id for which orders that don't have order_id
def pre_save_create_order_id(sender , instance, *args , **kwargs):
	if not instance.order_id:
		instance.order_id = unique_order_id_generator(instance)	#Function to create unique order id

pre_save.connect(pre_save_create_order_id , sender = Order)

# @receiver(post_save, sender = Order) << alternate way to connect post_save
#this receiver is executed when order object is saved so updating total
def post_save_order(sender, instance , created,  *args , **kwargs ):
	if created:
		instance.update_total()

post_save.connect(post_save_order, sender = Order)

# @receiver(post_save, sender = Cart)
#this receiver is executed after save to update cart total
def post_save_cart_total(sender, instance, *args, **kwargs):
	cart_obj = instance
	cart_total = cart_obj.total
	cart_id = cart_obj.id

	qs = Order.objects.filter(cart__id = cart_id) #here cart is foreign key in Order model that's why double_underscore is used

	if qs.count() == 1:
		order_obj = qs.first()
		order_obj.update_total()

post_save.connect(post_save_cart_total, sender = Cart)
