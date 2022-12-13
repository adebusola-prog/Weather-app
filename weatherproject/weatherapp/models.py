from django.db import models

# Create your models here.

# A visitor can save his email and a location. If a visitor successfully does this, the 
# app should send an email to the visitor with the weather condition of the location 
# sent every 6am. A visitor can unsubscribe from the email notification via a link in 
# the email

# make a model for email containing email nd location
# create a post(create) for the email and location
# Query the email and location for weather email to be sent to all the users based on the location

class Location(models.Model):
   location= models.CharField(max_length=300, blank=False, null=False)

   def __str__(self):
      return self.location

class EmailSubscription(models.Model):
   location= models.ForeignKey(Location, on_delete=models.SET_NULL, null= True)
   email= models.EmailField()
   is_subscribed= models.BooleanField(default=True)
   
   def __str__(self):
      return str(self.email) + "," + self.location.location

   
   
   