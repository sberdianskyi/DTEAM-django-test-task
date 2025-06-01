import os

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def send_cv_pdf_task(email, pdf_file_path, cv_name):
    # This task sends the CV PDF to the specified email address.
    subject = f"Your CV: {cv_name}"
    message = "Please find your CV attached."

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    print(f"PDF path: {pdf_file_path}")
    print(f"File exists: {os.path.exists(pdf_file_path)}")

    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "rb") as f:
            email.attach(f"{cv_name}.pdf", f.read(), "application/pdf")

    email.send(fail_silently=False)

    if os.path.exists(pdf_file_path):
        os.remove(pdf_file_path)
