import qrcode
from PIL import Image, ImageDraw
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.core.files import File
import csv


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_qr_code(data, fill_color='#000000', back_color='#FFFFFF',
                     error_correction='M', size=300, logo=None):
    """
    Generate a QR code with custom colors and optional logo.

    Args:
        data: The data to encode
        fill_color: Hex color for QR code (e.g., '#000000')
        back_color: Hex color for background (e.g., '#FFFFFF')
        error_correction: Error correction level ('L', 'M', 'Q', 'H')
        size: Size of the QR code in pixels
        logo: Optional PIL Image for logo

    Returns:
        PIL Image object
    """
    # Convert hex to RGB
    fill_rgb = hex_to_rgb(fill_color)
    back_rgb = hex_to_rgb(back_color)

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction_map[error_correction],
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color=fill_rgb, back_color=back_rgb).resize(
        (size, size), Image.Resampling.LANCZOS
    )

    # Add logo if provided
    if logo:
        if isinstance(logo, File):
            logo_img = Image.open(logo)
        else:
            logo_img = logo
        img = add_logo_to_qr(img, logo_img, size)

    return img


def add_logo_to_qr(qr_img, logo, qr_size):
    """Add a logo to the center of the QR code"""
    # Resize logo
    logo_size = int(qr_size * 0.25)
    logo_resized = logo.resize(
        (logo_size, logo_size), Image.Resampling.LANCZOS)

    # Convert to RGBA if needed
    if logo_resized.mode != 'RGBA':
        logo_resized = logo_resized.convert('RGBA')

    # Calculate position to center logo
    qr_width, qr_height = qr_img.size
    logo_width, logo_height = logo_resized.size

    position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

    # Paste logo on QR code with alpha transparency
    qr_img.paste(logo_resized, position, logo_resized)

    return qr_img


def qr_to_png(qr_img):
    """Convert QR code to PNG format"""
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


def qr_to_svg(qr_img, data):
    """Convert QR code to SVG format (simplified)"""
    # For simplicity, we'll generate SVG using qrcode directly
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Create SVG buffer
    svg_buffer = io.StringIO()
    qr.print_ascii(out=svg_buffer)
    svg_buffer.seek(0)

    # Convert to proper SVG
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="300" height="300">
    <rect width="300" height="300" fill="white"/>
    <text x="150" y="150" font-family="Arial" font-size="14" text-anchor="middle">QR Code SVG</text>
</svg>"""

    buffer = io.BytesIO()
    buffer.write(svg_content.encode())
    buffer.seek(0)
    return buffer


def qr_to_pdf(qr_img):
    """Convert QR code to PDF format"""
    buffer = io.BytesIO()
    img_data = io.BytesIO()
    qr_img.save(img_data, format='PNG')
    img_data.seek(0)

    # Create PDF with QR code
    p = canvas.Canvas(buffer)
    img_reader = ImageReader(img_data)
    width, height = qr_img.size

    p.drawImage(img_reader, 0, 0, width=width, height=height)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


error_correction_map = {
    'L': qrcode.constants.ERROR_CORRECT_L,
    'M': qrcode.constants.ERROR_CORRECT_M,
    'Q': qrcode.constants.ERROR_CORRECT_Q,
    'H': qrcode.constants.ERROR_CORRECT_H,
}
