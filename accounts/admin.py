from django.contrib import admin
from .models import UserProfile    # ModelClass must be called 

# Register your models here.
admin.site.register(UserProfile)  # registers to admin site 
