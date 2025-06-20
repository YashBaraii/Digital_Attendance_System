import qrcode
import os
from django.conf import settings
from django.core.mail import send_mail


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


# Bonus Feature 1: Email Notifications for Absences
def send_absence_alert(student, classroom):
    if student.email:
        send_mail(
            subject="Absence Alert",
            message=f"You missed today's session for {classroom.name}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=True,
        )
