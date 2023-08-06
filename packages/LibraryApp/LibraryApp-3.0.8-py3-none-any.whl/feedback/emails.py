from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from django.template.loader import render_to_string


def send_feedback_email(email, message):
    c = {'email': email, 'message': message}

    email_subject = render_to_string(
        'feedback/email/feedback_email_subject.html', c).replace('\n', '')
    email_body = render_to_string('feedback/email/feedback_email_body.html', c)

    email = EmailMessage(
        email_subject, email_body, email,
        [settings.DEFAULT_FROM_EMAIL], [],
        headers={'Reply-To': email}
    )
    return email.send(fail_silently=False)


def send_periodic_email():
    # send_mail(subject, message, from_email,
    # recipient_list, fail_silently=False,
    # auth_user=None, auth_password=None,
    # connection=None, html_message=None)
    send_mail(
        'Did you get this subject',  # subject
        'message: did you?.',        # message
        'kevin@example.com',          # sender
        ['she@example.com'],          # recipient
        fail_silently=False,         # raise exception if error
    )
