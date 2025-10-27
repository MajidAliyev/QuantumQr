from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, QRCode, Scan, BulkQRJob


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'qr_type', 'created_at']
    list_filter = ['qr_type', 'created_at']
    search_fields = ['name', 'data']


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ['qr_code', 'ip_address',
                    'country', 'device_type', 'scanned_at']
    list_filter = ['country', 'device_type', 'scanned_at']
    readonly_fields = ['scanned_at']


@admin.register(BulkQRJob)
class BulkQRJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'completed_at']
