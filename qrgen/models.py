from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import uuid


class User(AbstractUser):
    """Custom user model"""
    pass


class QRCode(models.Model):
    """QR Code model for static and dynamic codes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='qr_codes')
    name = models.CharField(max_length=200)
    qr_type = models.CharField(max_length=20, choices=[
        ('static', 'Static'),
        ('dynamic', 'Dynamic')
    ], default='static')

    # For static QR codes
    data = models.TextField(null=True, blank=True)

    # For dynamic QR codes
    short_url = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    destination_url = models.URLField(null=True, blank=True)

    # Design options
    fill_color = models.CharField(max_length=7, default='#000000')
    back_color = models.CharField(max_length=7, default='#FFFFFF')
    error_correction = models.CharField(max_length=1, choices=[
        ('L', 'Low - 7%'),
        ('M', 'Medium - 15%'),
        ('Q', 'Quartile - 25%'),
        ('H', 'High - 30%')
    ], default='M')
    size = models.IntegerField(default=300)

    # Logo
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('qr-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.short_url and self.qr_type == 'dynamic':
            self.short_url = self.generate_short_url()
        super().save(*args, **kwargs)

    def generate_short_url(self):
        """Generate a unique short URL"""
        import random
        import string
        while True:
            short = ''.join(random.choices(
                string.ascii_letters + string.digits, k=8))
            if not QRCode.objects.filter(short_url=short).exists():
                return short

    def get_scan_count(self):
        """Get total scan count for this QR code"""
        return self.scans.count()

    def get_data_url(self, request=None):
        """Get the data URL for this QR code"""
        if self.qr_type == 'static':
            return self.data
        else:
            # Use the request host dynamically so it works anywhere
            if request:
                host = request.get_host()
                scheme = request.scheme
                return f"{scheme}://{host}/redirect/{self.short_url}/"
            else:
                # Fallback for when request is not available
                return f"/redirect/{self.short_url}/"


class Scan(models.Model):
    """Model to track QR code scans"""
    qr_code = models.ForeignKey(
        QRCode, on_delete=models.CASCADE, related_name='scans')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scanned_at']


class BulkQRJob(models.Model):
    """Model to track bulk QR code generation jobs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    file = models.FileField(upload_to='bulk_csv/')
    result = models.FileField(upload_to='bulk_results/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
