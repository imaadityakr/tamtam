from django.contrib import admin
from .models import QRCodes

@admin.register(QRCodes)
class QRCodesAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'qrcode')
    list_filter = ('name','email')