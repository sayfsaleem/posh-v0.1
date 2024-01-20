# signals.py
import qrcode
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image
from .models import Product

@receiver(post_save, sender=Product)
def generate_qrcode(sender, instance, **kwargs):
    # Disconnect the signal temporarily to avoid recursion
    post_save.disconnect(generate_qrcode, sender=Product)

    try:
        # Generate QR code data
        qrcode_data = instance.barcode

        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qrcode_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"product_qrcodes/{instance.barcode}.png"

        # Save the QR code image
        img.save(img_path)

        # Resize the image and save it to the instance's qrcode field
        with open(img_path, "rb") as f:
            content = ContentFile(f.read())
            instance.qrcode.save(img_path, content, save=True)

    finally:
        # Reconnect the signal after processing
        post_save.connect(generate_qrcode, sender=Product)

        # Clean up: Delete the temporary QR code image
        img.close()
