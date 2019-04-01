from django.core.mail import send_mail


def sendEmail(subject, destinationemail, message):
    send_mail(
        subject,
        message,
        "develop@connectid.be",
        [destinationemail, ],
    )
