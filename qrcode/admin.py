from django.contrib import admin
from .models import UniqueID, QRCode

@admin.register(UniqueID)
class UniqueIDAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'expiry_date')
    list_filter = ('unique_code','expiry_date')

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('qr_id', 'name', 'email', 'contact')
    list_filter = ('qr_id','name')