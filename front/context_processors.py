#context processor is used to show same context in every webpage

from products.models import Product , SubCategory , Category
from accounts.models import UserProfile
from django.http import HttpResponse

#view function to show options in header area
def header_products(request):
	products  = Product.objects.all()
	subcategory = SubCategory.objects.all()

	category = Category.objects.all()

	context = {
				'products' : products,
				'subcategory' : subcategory,
				'category' : category
			}

	return context


#view function to show user icon in every webpage
def user_icon(request):
	if 'username' in request.session:
		user_data = UserProfile.objects.get(email = request.session.get('username'))
		context = { 'user_data' : user_data }

	else:
		context = { 'name' : "Nachiketa" }

	return context

