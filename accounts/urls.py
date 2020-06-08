from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

#from .views import RegisterUserView , UserLoginView , UpdateUserPassword

urlpatterns = [
    path('registration/', views.register_user ),
    path('login/', views.login ),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    path('guestregister/', views.guest_register),
    path('updatepassword/', views.update_password),

]
