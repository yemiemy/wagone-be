from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.models import User
from django.contrib.auth import authenticate


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")

        if username:
            user_qs = User.objects.filter(
                email__iexact=username, is_active=True
            )

            if not user_qs.exists():
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(
                    {"username": msg}, code="authorization"
                )
            user = user_qs.first()
        else:
            msg = _('Must include "username"')
            raise serializers.ValidationError(msg, code="authorization")

        user.last_login = timezone.now()
        user.save()
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        user.send_verification_email()
        token, _ = Token.objects.get_or_create(user=user)
        return token

    def delete(self):
        user = self.context["request"].user
        Token.objects.filter(user=user).delete()
