from celery import shared_task
from .models import BulkQRJob, QRCode
from .utils import generate_qr_code
import csv
import zipfile
import io
from PIL import Image
from django.core.files.base import ContentFile


@shared_task
def process_bulk_qr_code(job_id):
    """Process bulk QR code generation from CSV"""
    job = BulkQRJob.objects.get(id=job_id)
    job.status = 'processing'
    job.save()

    try:
        # Read CSV file
        csv_file = job.file.open('r')
        reader = csv.DictReader(csv_file)

        # Create ZIP file
        zip_buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(zip_buffer, 'w')

        qr_codes_created = []

        for row in reader:
            # Extract data from CSV
            name = row.get('name', 'QR Code')
            data = row.get('data', '')
            fill_color = row.get('fill_color', '#000000')
            back_color = row.get('back_color', '#FFFFFF')
            error_correction = row.get('error_correction', 'M')
            size = int(row.get('size', 300))

            if data:
                # Generate QR code
                qr_img = generate_qr_code(
                    data,
                    fill_color,
                    back_color,
                    error_correction,
                    size
                )

                # Convert to PNG
                img_buffer = io.BytesIO()
                qr_img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                # Add to ZIP
                zip_file.writestr(f'{name}.png', img_buffer.getvalue())

                # Create QR code record
                qr_code = QRCode.objects.create(
                    user=job.user,
                    name=name,
                    data=data,
                    qr_type='static',
                    fill_color=fill_color,
                    back_color=back_color,
                    error_correction=error_correction,
                    size=size,
                )
                qr_codes_created.append(qr_code)

        zip_file.close()

        # Save ZIP file
        zip_buffer.seek(0)
        job.result = ContentFile(zip_buffer.getvalue(), name='qr_codes.zip')
        job.status = 'completed'
        job.save()

    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.save()
        raise
