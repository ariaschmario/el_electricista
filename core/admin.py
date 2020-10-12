from django.contrib import admin

# Register your models here.
from core.models import Client, Ticket, GeneralInfo

admin.site.register(Client)
admin.site.register(Ticket)
admin.site.register(GeneralInfo)
