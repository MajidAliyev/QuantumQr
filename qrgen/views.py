import json
from .tasks import process_bulk_qr_code
from .utils import generate_qr_code, qr_to_png, qr_to_svg, qr_to_pdf
from .forms import QRCodeForm, QRCodeUpdateForm, BulkUploadForm
from .models import User, QRCode, Scan, BulkQRJob
import base64
import io
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')


def logout_view(request):
    """User logout"""
    auth_logout(request)
    return redirect('index')


def index(request):
    """Home page"""
    return render(request, 'index.html')


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


@login_required
def dashboard(request):
    """User dashboard with all QR codes"""
    qr_codes = QRCode.objects.filter(user=request.user)

    # Get statistics
    total_codes = qr_codes.count()
    static_codes = qr_codes.filter(qr_type='static').count()
    dynamic_codes = qr_codes.filter(qr_type='dynamic').count()
    total_scans = sum(code.get_scan_count() for code in qr_codes)

    # Recent activity
    recent_scans = Scan.objects.filter(qr_code__user=request.user)[:5]

    context = {
        'qr_codes': qr_codes,
        'total_codes': total_codes,
        'static_codes': static_codes,
        'dynamic_codes': dynamic_codes,
        'total_scans': total_scans,
        'recent_scans': recent_scans,
    }

    return render(request, 'dashboard.html', context)


@login_required
def create_qr(request):
    """Create a new QR code"""
    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            qr = form.save(commit=False)
            qr.user = request.user

            # Handle dynamic QR codes
            if qr.qr_type == 'dynamic':
                if qr.destination_url:
                    qr.save()
                else:
                    messages.error(
                        request, 'Please provide a destination URL for dynamic QR codes')
                    return render(request, 'create_qr.html', {'form': form})
            else:
                # Static QR codes
                if qr.data:
                    qr.save()
                else:
                    messages.error(
                        request, 'Please provide data for the QR code')
                    return render(request, 'create_qr.html', {'form': form})

            messages.success(request, 'QR code created successfully!')
            return redirect('qr-detail', pk=qr.pk)
    else:
        form = QRCodeForm()

    return render(request, 'create_qr.html', {'form': form})


@login_required
def qr_detail(request, pk):
    """View and download QR codes"""
    qr = get_object_or_404(QRCode, pk=pk, user=request.user)

    # Generate QR code image
    data_url = qr.get_data_url(request)

    # Get logo if exists
    logo = None
    if qr.logo:
        from PIL import Image
        logo = Image.open(qr.logo)

    qr_img = generate_qr_code(
        data_url,
        qr.fill_color,
        qr.back_color,
        qr.error_correction,
        qr.size,
        logo
    )

    # Save QR to bytes for response
    png_buffer = qr_to_png(qr_img)

    context = {
        'qr': qr,
        'qr_image_data': base64.b64encode(png_buffer.getvalue()).decode(),
        'scan_count': qr.get_scan_count(),
    }

    return render(request, 'qr_detail.html', context)


@login_required
@require_http_methods(["POST"])
def qr_preview(request):
    """HTMX endpoint for QR code preview"""
    data = request.POST.get('data')
    fill_color = request.POST.get('fill_color', '#000000')
    back_color = request.POST.get('back_color', '#FFFFFF')
    error_correction = request.POST.get('error_correction', 'M')
    size = int(request.POST.get('size', 300))

    if data:
        qr_img = generate_qr_code(
            data, fill_color, back_color, error_correction, size)
        png_buffer = qr_to_png(qr_img)
        qr_image_data = base64.b64encode(png_buffer.getvalue()).decode()

        return render(request, 'partials/qr_preview.html', {
            'qr_image_data': qr_image_data
        })

    return render(request, 'partials/qr_preview.html', {'qr_image_data': None})


@login_required
def download_qr(request, pk, format):
    """Download QR code in specified format"""
    qr = get_object_or_404(QRCode, pk=pk, user=request.user)
    data_url = qr.get_data_url(request)

    logo = None
    if qr.logo:
        from PIL import Image
        logo = Image.open(qr.logo)

    qr_img = generate_qr_code(
        data_url,
        qr.fill_color,
        qr.back_color,
        qr.error_correction,
        qr.size,
        logo
    )

    if format == 'png':
        buffer = qr_to_png(qr_img)
        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{qr.name}.png"'
        return response

    elif format == 'svg':
        buffer = qr_to_svg(qr_img, data_url)
        response = HttpResponse(buffer, content_type='image/svg+xml')
        response['Content-Disposition'] = f'attachment; filename="{qr.name}.svg"'
        return response

    elif format == 'pdf':
        buffer = qr_to_pdf(qr_img)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{qr.name}.pdf"'
        return response

    return redirect('qr-detail', pk=pk)


def redirect_qr(request, short_url):
    """Redirect short URL to destination URL"""
    qr = get_object_or_404(QRCode, short_url=short_url, qr_type='dynamic')

    # Log the scan
    log_scan(request, qr)

    # Redirect to destination URL
    return redirect(qr.destination_url)


def log_scan(request, qr_code):
    """Log QR code scan with analytics"""
    ip_address = request.META.get('REMOTE_ADDR', '')
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Parse user agent for device, browser, OS
    device_type = parse_device_type(user_agent)
    browser = parse_browser(user_agent)
    os = parse_os(user_agent)

    # GeoIP lookup (simplified - in production use MaxMind GeoIP2)
    country = get_country_from_ip(ip_address)
    city = get_city_from_ip(ip_address)

    Scan.objects.create(
        qr_code=qr_code,
        ip_address=ip_address,
        user_agent=user_agent,
        country=country,
        city=city,
        device_type=device_type,
        browser=browser,
        os=os,
    )


def parse_device_type(user_agent):
    """Parse device type from user agent"""
    ua_lower = user_agent.lower()
    if 'mobile' in ua_lower or 'android' in ua_lower:
        return 'Mobile'
    elif 'tablet' in ua_lower or 'ipad' in ua_lower:
        return 'Tablet'
    else:
        return 'Desktop'


def parse_browser(user_agent):
    """Parse browser from user agent"""
    if 'Chrome' in user_agent:
        return 'Chrome'
    elif 'Firefox' in user_agent:
        return 'Firefox'
    elif 'Safari' in user_agent:
        return 'Safari'
    elif 'Edge' in user_agent:
        return 'Edge'
    else:
        return 'Unknown'


def parse_os(user_agent):
    """Parse OS from user agent"""
    if 'Windows' in user_agent:
        return 'Windows'
    elif 'Mac' in user_agent:
        return 'macOS'
    elif 'Linux' in user_agent:
        return 'Linux'
    elif 'Android' in user_agent:
        return 'Android'
    elif 'iOS' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
        return 'iOS'
    else:
        return 'Unknown'


def get_country_from_ip(ip_address):
    """Get country from IP address"""
    # Simplified - in production use MaxMind GeoIP2 database
    return 'Unknown'


def get_city_from_ip(ip_address):
    """Get city from IP address"""
    # Simplified - in production use MaxMind GeoIP2 database
    return 'Unknown'


@login_required
def analytics(request, pk):
    """View analytics for a QR code"""
    qr = get_object_or_404(QRCode, pk=pk, user=request.user)
    scans = Scan.objects.filter(qr_code=qr)

    # Generate scan chart
    chart_data = generate_scan_chart(scans)

    # Device breakdown
    device_breakdown = scans.values('device_type').annotate(
        count=Count('device_type')
    ).order_by('-count')

    # Browser breakdown
    browser_breakdown = scans.values('browser').annotate(
        count=Count('browser')
    ).order_by('-count')

    # Country breakdown
    country_breakdown = scans.values('country').annotate(
        count=Count('country')
    ).order_by('-count')

    context = {
        'qr': qr,
        'total_scans': scans.count(),
        'chart_data': chart_data,
        'device_breakdown': device_breakdown,
        'browser_breakdown': browser_breakdown,
        'country_breakdown': country_breakdown,
    }

    return render(request, 'analytics.html', context)


def generate_scan_chart(scans):
    """Generate scan time series chart"""
    # Get last 30 days
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    # Aggregate scans by date
    recent_scans = scans.filter(scanned_at__gte=start_date)
    scan_by_date = {}

    for scan in recent_scans:
        date_str = scan.scanned_at.strftime('%Y-%m-%d')
        scan_by_date[date_str] = scan_by_date.get(date_str, 0) + 1

    # Create chart
    fig, ax = plt.subplots(figsize=(10, 4))

    if scan_by_date:
        dates = sorted(scan_by_date.keys())
        counts = [scan_by_date[d] for d in dates]
        ax.plot(dates, counts, marker='o', linewidth=2, markersize=6)
        ax.set_xlabel('Date')
        ax.set_ylabel('Scans')
        ax.set_title('Scans Over Last 30 Days')
        plt.xticks(rotation=45)
        plt.tight_layout()

    # Save to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return chart_data


@login_required
def bulk_upload(request):
    """Bulk upload QR codes from CSV"""
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            fill_color = form.cleaned_data.get('fill_color', '#000000')
            back_color = form.cleaned_data.get('back_color', '#FFFFFF')

            # Create job
            job = BulkQRJob.objects.create(
                user=request.user,
                file=csv_file,
                status='pending'
            )

            # Process asynchronously
            process_bulk_qr_code.delay(job.id)

            messages.success(
                request, 'Bulk QR code generation started. You will be notified when complete.')
            return redirect('bulk-jobs')
    else:
        form = BulkUploadForm()

    return render(request, 'bulk_upload.html', {'form': form})


@login_required
def bulk_jobs(request):
    """View bulk QR code generation jobs"""
    jobs = BulkQRJob.objects.filter(user=request.user)
    return render(request, 'bulk_jobs.html', {'jobs': jobs})


@login_required
@require_http_methods(["POST"])
def update_dynamic_url(request, pk):
    """HTMX endpoint to update dynamic QR code destination URL"""
    qr = get_object_or_404(QRCode, pk=pk, user=request.user)

    if qr.qr_type != 'dynamic':
        return JsonResponse({'error': 'Not a dynamic QR code'}, status=400)

    form = QRCodeUpdateForm(request.POST, instance=qr)
    if form.is_valid():
        form.save()
        return render(request, 'partials/url_display.html', {'qr': qr})

    return JsonResponse({'error': 'Invalid URL'}, status=400)


@login_required
def delete_qr(request, pk):
    """Delete a QR code"""
    qr = get_object_or_404(QRCode, pk=pk, user=request.user)
    qr.delete()
    messages.success(request, 'QR code deleted successfully!')
    return redirect('dashboard')
