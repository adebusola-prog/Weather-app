from django.contrib import admin
from .models import EmailSubscription, Location
# Register your models here.

admin.site.register(EmailSubscription)
admin.site.register(Location)