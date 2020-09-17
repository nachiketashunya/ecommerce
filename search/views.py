from django.shortcuts import render
from products.models import SubCategory, Product
from django.db.models import Q
# Create your views here.
# Q objects are used to execute more complex queries with OR statement

#View function to use search functionality
def search(request):
	method_dict = request.GET
	query = method_dict.get('search')	#name of search bar
	subcategory = SubCategory.objects.all()

	if query is not None:
		lookups = (Q (description__icontains = query) |							#icontains -- case insensitive, used with double(__)
					Q (brand_name__brand_name__icontains = query) |
					Q (title__icontains = query)
				)

		products = Product.objects.filter(lookups).distinct		#distince is used to prevent duplication
		context = {
					'products' : products,
					'subcategory' : subcategory,
					'title' : "Products"
				}

	else:
		products = Product.objects.all()

		context = {
					'products' : products,
					'subcategory' : subcategory,
					'title' : 'Products'
				}

	return render(request, 'front/productpage.html', context)


