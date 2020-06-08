from django.shortcuts import render
from products.models import SubCategory, Product
from django.db.models import Q 
# Create your views here.

def search(request):
	method_dict = request.GET
	query = method_dict.get('search')
	subcategory = SubCategory.objects.all()

	if query is not None:
		lookups = (Q (description__icontains = query) | 
					Q (brand_name__brand_name__icontains = query) | 
					Q (title__icontains = query)
				)

		products = Product.objects.filter(lookups).distinct
		context = { 'products' : products , 'subcategory': subcategory}

	else:
		products = Product.objects.all()
		context = { 'products' : products , 'subcategory': subcategory}

	return render(request, 'front/productpage.html', context)
 

