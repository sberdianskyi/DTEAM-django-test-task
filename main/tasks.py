import os
import logging

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_cv_pdf_task(email, pdf_file_path, cv_name):
    try:
        # This task sends the CV PDF to the specified email address.
        logger.info(f"Starting email task for {email} with CV: {cv_name}")
        subject = f"Your CV: {cv_name}"
        message = "Please find your CV attached."

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        logger.info(f"PDF path: {pdf_file_path}")
        logger.info(f"File exists: {os.path.exists(pdf_file_path)}")

        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, "rb") as f:
                email.attach(f"{cv_name}.pdf", f.read(), "application/pdf")
                logger.info(f"PDF file attached successfully")

        email.send(fail_silently=False)
        logger.info(f"Email sent successfully to {email}")

        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise
