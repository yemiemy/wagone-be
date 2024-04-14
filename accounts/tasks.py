import logging

from wagone_be.celery import app as celery_app
from django.conf import settings

from core.utils import send_template_email

logger = logging.getLogger(__name__)


def get_expiration_time():
    return int(settings.CACHES["default"]["TIMEOUT"] / 60)


@celery_app.task(name="send_account_otp_mail")
def send_account_otp_mail(first_name: str, email: str, otp_code: int):
    logger.info(
        "Sending account otp verification email for user: {}".format(email)
    )

    send_template_email(
        "account_otp.html",
        email,
        "Account OTP",
        **{
            "name": first_name,
            "account_name": email,
            "otp_code": otp_code,
            "expiration_time": get_expiration_time(),
        },
    )

    logger.info("OTP Verfication email sent to user: {}".format(email))
