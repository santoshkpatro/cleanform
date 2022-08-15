from typing import List
from cleanform.models.form import Form
from cleanform.models.submission import Submission
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.backends.filebased import EmailBackend as FileBasedEmailBackend
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from cleanform.models.responder import Responder
from cleanform.models.email_service import EmailService


@shared_task
def send_email_response(submission_id, submission_data):
    try:
        submission: Submission = Submission.objects.get(id=submission_id)
        form: Form = submission.form
        responders: List[Responder] = Responder.objects.filter(form=form)

        for responder in responders:
            email_service: EmailService = responder.email_service

            # Setting up Custom Email Sender
            email_sender = FileBasedEmailBackend(
                file_path=settings.BASE_DIR / 'log/responders'
            )

            # Email Message
            submission_email = EmailMessage(
                subject='Thankx for the new submission',
                body='Thankx for the new submission',
                from_email=responder.email,
                to=['hello@gmail.com'],
            )

            email_sender.send_messages([submission_email])



    except Submission.DoesNotExist:
        print('Submission Does Not Exist')