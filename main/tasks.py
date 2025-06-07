import os
import logging
import base64

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_cv_pdf_task(email, pdf_content_base64, cv_name):
    # This task sends the CV PDF to the specified email address.
    try:
        logger.info(f"Starting email task for {email} with CV: {cv_name}")

        # Decoding PDF from base64
        pdf_content = base64.b64decode(pdf_content_base64)

        # Checking that it is really PDF
        if not pdf_content.startswith(b"%PDF"):
            raise ValueError("Invalid PDF content")

        subject = f"Your CV: {cv_name}"
        message = "Please find your CV attached."

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        email.attach(f"{cv_name}.pdf", pdf_content, "application/pdf")
        logger.info(f"PDF file attached successfully")

        email.send(fail_silently=False)
        logger.info(f"Email sent successfully to {email}")

        return True

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise
