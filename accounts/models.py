from accounts.managers import UserManager
from accounts.utils import avatar_file_name, generate_code
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
from accounts.tasks import (
    send_account_otp_mail,
)
from core.utils import get_uuid


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=get_uuid, editable=False
    )  # type: ignore
    email = models.EmailField(_("email address"), unique=True, max_length=150)
    avatar = models.ImageField(
        upload_to=avatar_file_name, default="avatar.png"
    )
    birthday = models.DateField(blank=True, null=True)
    phone_number = PhoneNumberField(
        _("phone number"),
        blank=True,
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=settings.PHONENUMBER_REGEX_PATTERN,
                message="The phone number entered is not valid",
                code="invalid_phone_number",
            ),
        ],
    )
    is_email_verified = models.BooleanField(_("email verified"), default=False)
    is_phone_number_verified = models.BooleanField(
        _("phone number verified"), default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return self.get_full_name()

    def send_verification_email(self):
        Token.objects.get_or_create(user=self)
        verification_code = generate_code()
        cache.set(self.email, verification_code)

        send_account_otp_mail.delay(
            self.first_name, self.email, verification_code
        )

    def check_verification_pin(self, verification_code) -> bool:
        return cache.get(self.email) == verification_code

    def verify_account(self, verification_code) -> bool:
        if self.check_verification_pin(verification_code):
            self.is_email_verified = True
            self.save()
            Token.objects.get_or_create(user=self)
            # TODO: send a welcome email here, if need be
            cache.delete(self.email)
            return True
        return False


class UserContact(models.Model):
    id = models.UUIDField(primary_key=True, default=get_uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(
        User, related_name="contacts", blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.username}'s Contacts"
