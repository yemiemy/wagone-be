import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException


def get_uuid():
    return uuid.uuid4().hex


def get_uuid_hex(uuid_value):
    return (
        uuid.UUID(uuid_value).hex
        if type(uuid_value) is str
        else uuid_value.hex
    )


def custom_exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception
    Must be set in settings:
    # ...
    'EXCEPTION_HANDLER': 'mtp.apps.common.drf.exception_handler',
    # ...
    For the parameters, see ``exception_handler``
    """

    if (
        isinstance(exc, DjangoValidationError)
        or isinstance(exc, IntegrityError)
        or isinstance(exc, ObjectDoesNotExist)
    ):
        if hasattr(exc, "message_dict"):
            exc = DRFValidationError(detail=exc.message_dict)
        elif hasattr(exc, "message"):
            exc = DRFValidationError(
                detail={"non_field_errors": [exc.message]}
            )
        elif hasattr(exc, "messages"):
            exc = DRFValidationError(detail={"non_field_errors": exc.messages})
        else:
            exc = DRFValidationError(detail={"non_field_errors": [str(exc)]})
    elif type(exc) is Exception:
        exc = APIException(detail={"detail": exc.message})

    return drf_exception_handler(exc, context)


def send_template_email(template, email, subject, **context):
    if not isinstance(email, list):
        email = [email]
    context["email"] = "".join(email)
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        "WagOne <{}>".format(settings.EMAIL_HOST_USER),
        email,
        html_message=html_message,
    )
