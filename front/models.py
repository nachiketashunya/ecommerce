from django.db import models
from accounts.models import UserProfile
from products.models import Product


# Create your models here.

#manager to control wishlist products 
class WishlistManager(models.Manager):  #inherits the Manager class 
	def new_or_get(self, request):  #function to get new or old objects in wishlist
		wishlist_id = request.session.get('wishlist_id')
		qs = self.get_queryset().filter( id = wishlist_id)

		if qs.count() == 1 :
			obj_created = False 
			wishlist_obj = qs.first()

			if request.session.get('username') is not None and wishlist_obj.user is None:
				try:
					wishlist_obj.user = UserProfile.objects.get( email = request.session.get('username')).id
				except:
					wishlist_obj.user = None

			wishlist_obj.save()

		else:
			try:
				user = UserProfile.objects.get( email = request.session.get('username'))
			except:
				user = None 

			obj_created = True 

			wishlist_obj = Wishlist.objects.new(request , user = user )

			request.session['wishlist_id'] = wishlist_obj.id 

		return wishlist_obj , obj_created

	def new(self, request , user = None):
		user_obj = None

		if user is not None:
			if request.session.get('username'):
				user_obj = user 

		return self.model.objects.create( user = user_obj)

#model to store wishilist products 
class Wishlist(models.Model):
	user = models.ForeignKey(UserProfile , null = True , blank = True , on_delete = models.CASCADE)
	products = models.ManyToManyField(Product , blank = True)
	objects = WishlistManager()  #manager to control wishlist objects


