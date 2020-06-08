from django.db import models
import random 
import os
# Create your models here.
def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name,ext = os.path.splitext(base_name)

	return name, ext 

def upload_product_image(instance , filename):
	new_filename = random.randint(1, 456890674)
	name, ext = get_filename_ext(filename)
	final_filename = f"{new_filename},{ext}" 

	return 'MyProductImage/' + f"{new_filename}/{final_filename}"

ACTIVE_CHOICE = (('active' , 'Active'), ('deactive' ,'Deactive'))


#Brand model for information about product's brand
class Brand(models.Model):
	brand_name = models.CharField(max_length = 80)
	brand_image = models.ImageField( null = True , blank = True)

	def __str__(self):
		return self.brand_name

#Category model for information about product's category
class Category(models.Model):
	category_name = models.CharField(max_length = 80)
	category_image = models.ImageField( null = True, blank = True)

	def __str__(self):
		return self.category_name

#SubCategory model for information about product's subcategory
class SubCategory(models.Model):
	category_name = models.ForeignKey(Category , on_delete = models.CASCADE)
	subcategory_name = models.CharField(max_length = 80)
	subcategory_image = models.ImageField(null = True , blank = True)

	def __str__(self):
		return self.subcategory_name 


#Product model to store products in database 
class Product(models.Model):
	title = models.CharField(max_length = 80)
	description = models.TextField( max_length = 800)
	slug = models.SlugField( null = True , blank = True)
	active = models.BooleanField(default = True)
	price = models.DecimalField( max_digits = 15 , decimal_places = 2)
	brand_name = models.ForeignKey(Brand, on_delete = models.CASCADE)  #ForeignKey to grab the info from Brand
	subcategory_name = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
	image = models.ImageField( unique = True , upload_to = upload_product_image)

	def __str__(self):
		return self.title 

	def get_absolute_url(self):
		return reverse('products:product_detail' , kwargs = { 'pk' : self.pk })

#Review model to store reviews in database 
class Review(models.Model):
	reviewed_by = models.EmailField()
	product_id = models.IntegerField()
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True )
	updated_at = models.DateTimeField(auto_now = True)

	class Meta:
		#this is to decide constraints that one product_id gets only one review from a single user 
		constraints = [ models.UniqueConstraint(fields = ['reviewed_by' , 'product_id'], name = 'ReviewConstraints')]

	def __str__(self):
		return self.reviewed_by

