from django.contrib import admin
from myapp.models import Client, AdventureType, Adventure, CreateEvent, EventBooking

# Register your models here.

admin.site.register(Client)
admin.site.register(AdventureType)
admin.site.register(Adventure)
admin.site.register(CreateEvent)
admin.site.register(EventBooking)

