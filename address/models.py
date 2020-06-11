from django.db import models
from billing.models import BillingProfile

# Create your models here.
ADDRESS_TYPE = (('shipping' ,'Shipping'), ('billing', 'Billing'))


# ModelClass to store address for order
class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete = models.CASCADE)
	address_type = models.CharField(max_length = 20, choices = ADDRESS_TYPE)
	address_line_1 = models.CharField(max_length= 130)
	address_line_2 = models.CharField(max_length = 120)
	city = models.CharField(max_length = 30)
	state = models.CharField(max_length = 30)
	pincode = models.CharField(max_length = 8)
	country  = models.CharField(max_length = 30, default = "India")

	def __str__(self):
		return self.billing_profile.email




