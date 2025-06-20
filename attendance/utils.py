import qrcode
import os
from django.conf import settings


def generate_qr(session):
    data = str(session.session_id)
    qr = qrcode.make(data)

    file_path = os.path.join(
        settings.MEDIA_ROOT, "qr_codes", f"{session.session_id}.png"
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    qr.save(file_path)
    session.qr_code_image = f"qr_codes/{session.session_id}.png"
    session.save()
