from django.urls import path
from . import views 

urlpatterns = [
	path('checkout_address/' , views.checkout_address),
	path('checkout_address_reuse/', views.checkout_address_reuse),
]