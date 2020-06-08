from products.models import Product , SubCategory , Category
from accounts.models import UserProfile 
from django.http import HttpResponse


def header_products(request ):
	products  = Product.objects.all()
	subcategory = SubCategory.objects.all()

	category = Category.objects.all()

	context = {
				'products' : products,
				'subcategory' : subcategory,
				'category' : category
			}

	return context
	

def user_icon(request):
	if 'username' in request.session:
		user_data = UserProfile.objects.get(email = request.session.get('username'))
		print(user_data)
		context = { 'user_data' : user_data }

	else:
		context = { 'name' : "Nachiketa" }

	return context

