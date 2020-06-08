from django.urls import path
from . import views 

urlpatterns = [
	path('cart/', views.cart),
	path('cart/cartupdate/', views.cartupdate),
	path('cart/checkout/' , views.checkout),
	path('cart/successful/', views.successful),
]