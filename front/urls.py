from django.urls import path
from . import views 
from .views import ProductPageView , ProductDetailView , ProductCategoryView


app_name = "products"

urlpatterns = [
	path('', views.home),  
	path('productpage/',views.productpage),
	path('productdetails/<id>', views.productdetails),
	path('productcategory/<id>', views.productcategory),
	path('wishlist/' , views.wishlist),
	path('wishlist_update/', views.wishlist_update),
	path('profile/' , views.profile),
	path('aboutus/' , views.about_us),
	path('header_products/<id>', views.header_products),


	# Class Based Urls 

	path('productpageview/' , ProductPageView.as_view() , name = "productpage"),
	path('productdetailview/<int:pk>' , ProductDetailView.as_view(), name = "product_detail"),
	path('productcategoryview/<int:id>' , ProductCategoryView.as_view() , name = "product_category"),

]