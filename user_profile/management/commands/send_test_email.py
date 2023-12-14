from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends a test email using Gmail SMTP'

    def handle(self, *args, **options):
        subject = 'Test Email'
        message = 'This is a test email sent from Django.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = ['monirul.developers@gmail.com']  # Replace with the recipient's email address

        send_mail(subject, message, from_email, to_email, fail_silently=False)
        self.stdout.write(self.style.SUCCESS('Test email sent successfully.'))
