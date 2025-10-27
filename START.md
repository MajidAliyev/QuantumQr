# QuantumQR - Startup Guide

## 🚀 Quick Start

The QuantumQR application is ready to use! Here's how to get started:

### 1. Start the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the server
python manage.py runserver

# Or use the run script
./run.sh
```

The application will be available at: **http://localhost:8000**

### 2. Access the Application

- **Home Page**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### 3. Create a User

First time users need to register:

1. Click "Register" in the navigation
2. Fill in username, email, and password
3. You'll be automatically logged in

Or create a superuser for admin access:

```bash
python manage.py createsuperuser
```

## 📊 Features Implemented

### ✅ Core Features

- ✅ User authentication system
- ✅ Static QR code generation
- ✅ Dynamic QR codes with URL updating
- ✅ Scan analytics with device breakdown
- ✅ Multiple export formats (PNG, SVG, PDF)
- ✅ Custom colors and logos
- ✅ Error correction levels
- ✅ Live preview with HTMX
- ✅ Bulk CSV processing
- ✅ Server-rendered charts with Matplotlib

### ✅ HTMX Features (Zero JavaScript)

- ✅ Live QR code preview as you type
- ✅ Inline URL updates for dynamic codes
- ✅ Instant form updates without page reload

### ✅ Tailwind CSS UI

- ✅ Modern, responsive design
- ✅ Professional gradient navigation
- ✅ Clean, intuitive interface
- ✅ Mobile-friendly layout

## 🎨 Using the Application

### Creating a Static QR Code

1. Log in to your account
2. Navigate to "Create QR Code"
3. Fill in the form:
   - Enter a name for your QR code
   - Select "Static" type
   - Enter your data (URL, text, etc.)
   - Customize colors (click the color picker)
   - Set error correction level
   - Adjust size (100-1000 pixels)
   - (Optional) Upload a logo
4. Watch the live preview update as you type
5. Click "Create QR Code"
6. Download in PNG, SVG, or PDF format

### Creating a Dynamic QR Code

1. Navigate to "Create QR Code"
2. Select "Dynamic" type
3. Enter the destination URL
4. Create the QR code
5. Share the short URL - it never changes!
6. Update the destination URL anytime without reprinting

### Viewing Analytics

1. Click on any QR code from your dashboard
2. Navigate to "Analytics" tab
3. See:
   - Total scans
   - Device breakdown (Mobile/Desktop/Tablet)
   - Browser usage
   - Geographic data
   - Scan trends chart

### Bulk Processing

1. Prepare a CSV file with columns: `name,data`
   ```csv
   name,data
   Product A,https://example.com/product-a
   Product B,https://example.com/product-b
   ```
2. Go to "Bulk Upload"
3. Upload CSV file
4. Choose colors and settings
5. Monitor progress in "Bulk Jobs"
6. Download ZIP file when complete

## 🔧 Optional: Background Tasks with Celery

For bulk processing, you'll need Redis and Celery:

1. **Install Redis** (if not installed):

   ```bash
   brew install redis  # macOS
   # or
   sudo apt-get install redis  # Linux
   ```

2. **Start Redis**:

   ```bash
   redis-server
   ```

3. **Start Celery Worker** (in a new terminal):
   ```bash
   cd "/Users/majid/Desktop/QR Code Generator"
   source venv/bin/activate
   celery -A quantumqr worker --loglevel=info
   ```

## 📁 Project Structure

```
QuantumQR/
├── quantumqr/           # Django project settings
│   ├── settings.py     # App configuration
│   ├── urls.py         # URL routing
│   └── celery.py       # Celery configuration
├── qrgen/              # Main application
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── forms.py        # Form definitions
│   ├── utils.py        # QR code utilities
│   ├── tasks.py        # Celery background tasks
│   └── urls.py         # App URL routing
├── templates/          # HTML templates
├── static/             # Static files
├── media/              # User uploads
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## 🎯 Key Endpoints

- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/dashboard/` - User dashboard
- `/create/` - Create QR code
- `/qr/<id>/` - View QR code details
- `/qr/<id>/analytics/` - View analytics
- `/redirect/<short_url>/` - Dynamic QR redirect
- `/bulk-upload/` - Bulk CSV upload
- `/bulk-jobs/` - View bulk jobs

## 🐛 Troubleshooting

### Cannot access admin panel

Create a superuser:

```bash
python manage.py createsuperuser
```

### Database errors

Run migrations:

```bash
python manage.py migrate
```

### Static files not loading

Collect static files:

```bash
python manage.py collectstatic
```

## 📝 Notes

- The application uses SQLite by default (perfect for development)
- For production, use PostgreSQL and update settings.py
- GeoIP features require MaxMind GeoIP2 database (can be added later)
- HTMX handles all frontend interactivity - no JavaScript needed!
- All charts and analytics are server-rendered with Matplotlib

## 🎉 Enjoy!

You now have a fully functional QR code generator with analytics, HTMX interactivity, and modern UI!

For questions or issues, check the README.md file for more details.
