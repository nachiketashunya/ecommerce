from django.shortcuts import render, redirect
from products.models import Product , Review, SubCategory, Category
from django.http import HttpResponse
from products.forms import ReviewForm
from django.core.paginator import Paginator
from cart.models import Cart
from front.models import Wishlist, WishlistManager
from accounts.models import UserProfile

from django.views.generic import ListView , View


#from django.views.decorators.cache import cache_page
#from django.views.generic import View , ListView  , DetailView


# Create your views here.

# view function to show products
# first argument is always request

def productpage(request):
	products = Product.objects.all().order_by('subcategory_name') #fetching queryset of all products ordered by subcategory_name
	subcategory = SubCategory.objects.all()  #fetching queryset of all subcategories

	next_url = request.build_absolute_uri  #building reverse url

	wishlist_obj , obj_created = Wishlist.objects.new_or_get(request)

	context = {
				'products' : products,
				'subcategory': subcategory,
				'object' : wishlist_obj,
				'next_url' : next_url,
				'title' : 'Products'  #this will be used as a title of the webpage
			}


	return render(request, 'front/productpage.html' , context) #request is first argument, template name is second, context is optional


def home(request):
	return render(request, 'front/home.html' , { 'title' : 'Home'})


# view function to show the details of product, it wil get 'id' from url
def productdetails(request, id):
	if 'username' not in request.session:  # checking for username
		form = ReviewForm( request.POST or None)
	else:
		#providing initial so that some fields are automatically filled out
		form = ReviewForm(request.POST or None, initial = { 'reviewed_by': request.session['username'], 'product_id' : id})

	if request.method == "POST":
		if form.is_valid():
			reviewed_by = form.cleaned_data.get('reviewed_by')
			description = form.cleaned_data.get('description')
			review = Review(reviewed_by = reviewed_by, description = description, product_id = id)
			try:
				review.save()
				return redirect('/productdetails/<id>')
			except:
				return redirect('/unsuccessful')



	try:
		product = Product.objects.get(id = id)  #fetching an object of matching id
		reviews_list = Review.objects.filter(product_id = id).order_by('id') #filtering querset by product id
		paginator = Paginator(reviews_list , 1)  # Paginator is used to split tons of objects into multiple pages
		page = request.GET.get('page')
		reviews = paginator.get_page(page)
		cart_obj, new_obj = Cart.objects.new_or_get(request)

		context = { 'title' : 'productdetails',
		            'product': product ,
		            'form' : form,
		            'reviews' : reviews,
		            'cart' : cart_obj
		        }

		return render(request, 'front/productdetails.html', context)

	except:
		return HttpResponse("<h1>Product Not Found</h1>")

# view function to show products category wise
def productcategory(request, id):
	products = Product.objects.filter(subcategory_name = id)
	subcategory = SubCategory.objects.all()

	context = {
				'products' : products,
				'subcategory': subcategory,
				'title' : 'Products'
			}

	return render(request, 'front/productpage.html' , context)

# view function to show wishlist
def wishlist(request):
	wishlist_obj , obj_created = Wishlist.objects.new_or_get(request)

	cart_obj , obj_created = Cart.objects.new_or_get(request)

	context = {
				'object' : wishlist_obj,
				'cart' : cart_obj,
				'title' : 'Wishlist'
			}

	return render(request, 'front/wishlist.html' , context)

#view function to control update in wishlist
def wishlist_update(request):
	product_id = request.POST.get('product_id')  #getting product_id from POST request

	next_ = request.POST.get('next')
	next_url = request.GET.get('next')
	redirect_path = next_ or next_url or None


	if product_id is not None:
		try:
			product_obj = Product.objects.get( id = product_id)  #matching product object

		except request.DoesNotExist:
			return redirect('/productpage')

		wishlist_obj, obj_created = Wishlist.objects.new_or_get(request)  #getting wishlist object

		if product_obj in wishlist_obj.products.all():
			wishlist_obj.products.remove(product_obj) #if product is already in wishlist then remove it

		else:
			wishlist_obj.products.add( product_obj)  #else add it

		request.session['wishlist_items'] = wishlist_obj.products.count() #set wishlist_items in session

	return redirect(redirect_path)

# view function to show the profile of user
def profile(request):
	if request.session.get('username'):
		user = UserProfile.objects.get( email = request.session.get('username'))

		context = {
					'user' : user ,
					'title' : "Profile"
				}

		return render(request , 'front/profile.html' , context)

	return redirect('/login')

# view function to show about us
def about_us(request):
	return render(request , 'base/about.html')



	"""   Class Based Views   """

class ProductPageView(ListView):
	template_name = 'front/productpage.html'

	#context_object_name = "products"

	def get_queryset(self):
		products = Product.objects.all().order_by('subcategory_name')
		subcategory = SubCategory.objects.all()


		queryset = {
						'products' : products ,
						'subcategory' : subcategory
					}

		return queryset

	def get_context_data(self , **kwargs):
		context = super().get_context_data(**kwargs)
		self.next_url = self.request.build_absolute_uri


		context['title'] = "Products"
		context['next_url'] = self.next_url

		return context

class ProductDetailView(View):
	form_class = ReviewForm

	def get(self, request , *args, **kwargs):
		product_id = self.kwargs['pk']

		if 'username' not in request.session:
			form = self.form_class()

		else:
			form = self.form_class(initial = {
												'reviewed_by' : self.request.session['username'],
												'product_id' : product_id
											})

		try:
			product = Product.objects.get(pk = product_id)
			reviews_list = Review.objects.filter(product_id = product_id ).order_by('id')
			paginator = Paginator(reviews_list , 1)
			page = request.GET.get('page')
			reviews = paginator.get_page(page)

			cart_obj , new_obj = Cart.objects.new_or_get(request)

			context = { 'title' : 'productdetails',
		            'product': product ,
		            'form' : form,
		            'reviews' : reviews,
		            'cart' : cart_obj
		        }


			return render(request , 'front/productdetails.html' , context)

		except:
			return HttpResponse("<h1> Product Not Found </h1>")


	def post(self , request, *args ,**kwargs):
		product_id = self.kwargs.get('pk')

		if 'username' not in request.session:
			form = self.form_class()

		else:
			form = self.form_class(request.POST , initial = {
												'reviewed_by' : self.request.session['username'],
												'product_id' : product_id
											})

		if form.is_valid():
			reviewed_by = form.cleaned_data.get('reviewed_by')
			description = form.cleaned_data.get('description')

			review = Review( reviewed_by = reviewed_by , description = description , product_id = product_id)

			try:
				review.save()

				return redirect('/productpageview')
			except:
				return redirect('/productpageview')



class ProductCategoryView(ListView):
	template_name = "front/productpage.html"

	def get_queryset(self):
		products = Product.objects.filter( subcategory_name = self.kwargs['id'])

		subcategory = SubCategory.objects.all()

		queryset = {
					'products' : products ,
					'subcategory': subcategory
				}

		return queryset



