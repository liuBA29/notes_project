from django.contrib import admin
from .models import ContactInfo, Client, ClientCard, CallRecord

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'image')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(ClientCard)
class ClientCardAdmin(admin.ModelAdmin):
    list_display = ('client', 'is_primary', 'created_at')

@admin.register(CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    list_display = ('channel', 'calling_number', 'state', 'created_at')
    list_filter = ('state',)
