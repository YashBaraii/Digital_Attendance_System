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

    subject = "Absence Alert"
    message = (
        f"Dear {student.username},\n\nYou missed today's session for: {classroom.name}."
    )

    try:
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=False,  # Enable to raise real errors for now
        )
    except Exception as e:
        print(f"Email sending failed: {e}")
        return 0
