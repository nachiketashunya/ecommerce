from django.db import models  # All model class subclasses django.db.models.Model 
import random 
import os 

# Create your models here.

GENDER_CHOICE = (('male', 'Male'), ('female', 'Female')) # First Value -- Database , Second Value --- User will See 


def get_filename_ext(filepath):
	base_name = os.path.basename(filepath) # Get Base Name 
	name,ext = os.path.splitext(base_name) # Get name and extension 

	return name, ext 

def upload_profile_image(instance , filename):
	new_filename = random.randint(1, 456890674)
	name, ext = get_filename_ext(filename)
	final_filename = f"{new_filename},{ext}"  # This formats the final_filename  

	return 'UserProfileImage/' + f"{new_filename}/{final_filename}"


class UserProfile(models.Model):  # We inherit Model class so that it can act like a Model 
	name 			 = models.CharField(max_length = 80)  # max_length == required 
	phone_no 		 = models.CharField(max_length = 10, unique = True) # It can't be duplicated 
	email		 	 = models.EmailField(unique = True)
	gender 		     = models.CharField(max_length = 8, choices = GENDER_CHOICE)
	password 		 = models.CharField(max_length = 20)
	confirm_password = models.CharField( max_length = 20)
	profile_image 	 = models.ImageField(
											unique = True ,  
											blank = True , # blank -- Validation Related
											null = True , # null -- Database Related 
											upload_to = upload_profile_image) # Calling Function 



	def __str__ ( self):  # Magic Method -- Converts model objects into string 
		return self.name 

class GuestEmail(models.Model):
	email = models.EmailField()
	active = models.BooleanField(default = True)
	updated_at = models.DateTimeField( auto_now = True) # DateTimeField can also be specified 
	created_at = models.DateTimeField( auto_now_add = True)

	def __str__(self):
		return self.email 


print("MY name ")

