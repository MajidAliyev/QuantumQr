# QuantumQR - Dynamic QR Code Generator

A full-stack web application for generating dynamic QR codes with analytics, built with Django, HTMX, and Tailwind CSS.

## Features

- **Zero JavaScript Core Logic**: All interactivity handled via HTMX
- **Custom QR Code Generation**: Full color control, logo insertion, multiple formats
- **Dynamic QR Codes**: Update destination URLs without changing the QR image
- **Scan Analytics**: Track scans with device, browser, and geographic insights
- **Server-Rendered Charts**: Visualization using Matplotlib
- **Bulk Processing**: CSV upload with background task processing
- **Modern UI**: Beautiful interface built with Tailwind CSS

## Tech Stack

- **Backend**: Django 4.2
- **Frontend**: Tailwind CSS + HTMX (zero JavaScript for core logic)
- **QR Code Generation**: qrcode + Pillow
- **Export Formats**: PNG, SVG, PDF
- **Background Tasks**: Celery + Redis
- **Analytics**: Matplotlib
- **Database**: SQLite (dev) / PostgreSQL (production)

## Installation

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:

```bash
python manage.py createsuperuser
```

5. Start Redis (required for Celery):

```bash
redis-server
```

6. Start Celery worker (in a new terminal):

```bash
celery -A quantumqr worker --loglevel=info
```

7. Start Django development server:

```bash
python manage.py runserver
```

## Usage

### Creating Static QR Codes

1. Navigate to "Create QR Code"
2. Enter your data (URL, text, etc.)
3. Customize colors, error correction, and size
4. Optionally upload a logo
5. Download in PNG, SVG, or PDF format

### Creating Dynamic QR Codes

1. Navigate to "Create QR Code"
2. Select "Dynamic" type
3. Enter the destination URL
4. Generate and share the short URL
5. Update destination URL anytime without reprinting

### Bulk Processing

1. Prepare a CSV file with columns: `name,data`
2. Navigate to "Bulk Upload"
3. Upload CSV file
4. Monitor progress in "Bulk Jobs"
5. Download ZIP file when complete

## Project Structure

```
quantumqr/
├── quantumqr/          # Django project settings
├── qrgen/              # Main application
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── forms.py        # Form definitions
│   ├── utils.py        # QR code generation utilities
│   ├── tasks.py        # Celery background tasks
│   └── urls.py         # URL routing
├── templates/          # HTML templates
├── static/             # Static files
└── media/              # User uploads
```

## API Endpoints

- `/` - Home page
- `/dashboard/` - User dashboard
- `/create/` - Create QR code
- `/qr/<id>/` - View QR code details
- `/qr/<id>/download/<format>/` - Download QR code
- `/qr/<id>/analytics/` - View scan analytics
- `/redirect/<short_url>/` - Redirect dynamic QR codes
- `/bulk-upload/` - Bulk CSV upload
- `/bulk-jobs/` - View bulk jobs

## HTMX Endpoints

- `/qr/preview/` - Live QR code preview
- `/qr/<id>/update-url/` - Update dynamic URL

## License

MIT License
