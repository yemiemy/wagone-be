from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from accounts.models import User, UserContact
from accounts.utils import generate_random_password

import logging

logger = logging.getLogger(__name__)


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "avatar",
            "birthday",
            "phone_number",
            "email",
            "last_login",
        )
        read_only_fields = (
            "id",
            "last_login",
        )


class UserAccountSerializer(UserBaseSerializer):

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + (
            "email",
            "is_email_verified",
            "is_phone_number_verified",
        )
        read_only_fields = UserBaseSerializer.Meta.read_only_fields + (
            "is_email_verified",
            "is_phone_number_verified",
        )
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        user_qs = User.objects.filter(email__iexact=value)
        if user_qs.exists():
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )
        else:
            return value

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["password"] = generate_random_password()
            user = User.objects.create_user(**validated_data)
            UserContact.objects.get_or_create(user=user)

            Token.objects.get_or_create(user=user)
            user.send_verification_email()
            return user


class UserAccountVerificationSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(
        max_value=999999, min_value=100000
    )
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs["email"]
        verification_code = attrs["verification_code"]

        user_qs = User.objects.filter(email__iexact=email, is_active=True)
        if not user_qs.exists():
            raise serializers.ValidationError(
                {"email": ["user with this email address does not exist."]}
            )
        user = user_qs.first()
        if not user.check_verification_pin(verification_code):
            raise serializers.ValidationError(
                {"verification_code": _("Invalid verification code.")}
            )
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        verified = user.verify_account(validated_data["verification_code"])
        if not verified:
            raise serializers.ValidationError(
                {
                    "verification_code": _(
                        "Verification code expired. Resend verification email \
                            to get new verification code."
                    )
                }
            )
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save()
        return {"token": token.key}


class RegenerateVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        user_qs = User.objects.filter(email__iexact=email, is_active=True)
        if not user_qs.exists():
            raise serializers.ValidationError(
                {"email": ["user with this email address does not exist."]}
            )
        return user_qs.first()

    def create(self, validated_data):
        user = validated_data["email"]
        user.send_verification_email()
        return True


class UpdateUserAccountEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        user_qs = User.objects.filter(email__iexact=email)
        if user_qs.exists():
            raise serializers.ValidationError(
                "user with this email address already exists."
            )
        else:
            return email

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.username = validated_data["email"]
        instance.is_email_verified = False
        instance.send_verification_email()
        instance.save()
        Token.objects.filter(user=instance).delete()
        return instance


class UpdateUserAccountNameSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=True, max_length=254)
    last_name = serializers.CharField(allow_blank=True, max_length=254)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.save()
        return instance


class AccountDeletionSerializer(serializers.Serializer):
    hard = serializers.BooleanField(
        write_only=True, required=False, default=False
    )  # type: ignore

    def create(self, validated_data):
        hard_delete = validated_data["hard"]
        user = self.context["request"].user

        if hard_delete:
            user.delete()
        else:
            user.is_active = False
            user.save()
        return True


class UserContactSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    contacts = UserAccountSerializer(many=True)

    class Meta:
        model = UserContact
        fields = (
            "id",
            "user",
            "contacts",
        )
        read_only_fields = (
            "id",
            "user",
            "contacts",
        )
