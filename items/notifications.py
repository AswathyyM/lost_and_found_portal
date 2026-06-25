from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail


EMAIL_SENT = 'sent'
EMAIL_MISSING_CONFIG = 'missing_config'
EMAIL_MISSING_OWNER = 'missing_owner_email'
EMAIL_SEND_FAILED = 'send_failed'


def is_placeholder(value):
    return value.startswith('replace_with_')


def send_item_claimed_email(item, claimer):
    owner_email = item.owner.email
    from_email = settings.DEFAULT_FROM_EMAIL

    if not owner_email:
        return EMAIL_MISSING_OWNER

    if not from_email or is_placeholder(from_email):
        return EMAIL_MISSING_CONFIG

    if (
        not settings.EMAIL_HOST_USER
        or is_placeholder(settings.EMAIL_HOST_USER)
        or not settings.EMAIL_HOST_PASSWORD
        or is_placeholder(settings.EMAIL_HOST_PASSWORD)
    ):
        return EMAIL_MISSING_CONFIG

    claimer_email = claimer.email or 'No email provided'

    subject = f'Your item "{item.title}" was claimed'
    message = (
        f'Hello {item.owner.username},\n\n'
        f'{claimer.username} has claimed your item "{item.title}".\n\n'
        f'Item details:\n'
        f'Type: {item.item_type}\n'
        f'Location: {item.location}\n'
        f'Contact on listing: {item.contact}\n\n'
        f'Claimed by:\n'
        f'Username: {claimer.username}\n'
        f'Email: {claimer_email}\n\n'
        f'Please contact the student to verify and complete the handover.\n\n'
        f'CEC Lost And Found'
    )

    try:
        send_mail(
            subject,
            message,
            from_email,
            [owner_email],
            fail_silently=False
        )
    except (SMTPException, OSError, ValueError):
        return EMAIL_SEND_FAILED

    return EMAIL_SENT
