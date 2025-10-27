# QuantumQR

Generate dynamic QR codes with instant URL updates, scan analytics, and zero JavaScript.

I built this because I wanted QR codes that I could update without printing new ones. The URL changes, but the QR code image stays the same.

## What It Does

**Dynamic QR Codes** - The main feature. Print once, update the URL forever.

You create a QR code that points to a short URL like `your-domain.com/redirect/abc123/`.
When someone scans it, they get redirected to wherever you set it. The best part?
You can change where it points anytime without making a new QR code.

**Also includes**:

- Custom colors and logos on QR codes
- Track who scans them (devices, browsers, locations)
- See charts of scan activity over time
- Bulk generate QR codes from CSV files
- Download in PNG, SVG, or PDF

## What I Built It With

- Django for the backend
- HTMX for the frontend (no JavaScript needed)
- Tailwind CSS for styling
- Matplotlib for analytics charts
- Celery handles bulk processing in the background

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

That's it! Open http://localhost:8000 in your browser.

## How It Works

**Static QR codes**: Put in text/URL, get a QR code. Simple.

**Dynamic QR codes**: This is where it gets interesting.

1. Create a dynamic QR code with a destination URL
2. You get a short URL like `yoursite.com/redirect/abc123/`
3. Share that short URL or print the QR code
4. Anytime you want, log in and change where it points
5. The QR code image never changes, but the destination does

This means you can print menus, business cards, posters, and update them instantly without reprinting.

## Deployment

Deploy to Render, Railway, or Fly.io. All the configs are already in the repo.

Read `DEPLOY_TO_YOUR_DOMAIN.md` for the full guide.

## License

This project is private and not licensed for public use.


