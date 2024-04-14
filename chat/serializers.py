from django.db.models import Q
from rest_framework import serializers
from chat.models import Chat, Message
from accounts.models import User


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "receiver",
            "chat",
            "content",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class ChatSerializer(serializers.ModelSerializer):
    user1_id = serializers.UUIDField(write_only=True)
    user2_id = serializers.UUIDField(write_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "user1",
            "user2",
            "user1_id",
            "user2_id",
            "messages",
            "created_at",
        )
        read_only_fields = (
            "id",
            "user1",
            "user2",
            "messages",
            "created_at",
        )

    def validate_user1_id(self, user1_id):
        user_qs = User.objects.filter(id=user1_id, is_active=True)
        if not user_qs.exists():
            raise serializers.ValidationError(f"No user with id '{user1_id}'")
        return user_qs.first()

    def validate_user2_id(self, user2_id):
        user_qs = User.objects.filter(id=user2_id, is_active=True)
        if not user_qs.exists():
            raise serializers.ValidationError(f"No user with id '{user2_id}'")
        return user_qs.first()

    def create(self, validated_data):
        user1 = validated_data["user1_id"]
        user2 = validated_data["user2_id"]

        chat_qs = Chat.objects.filter(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        )
        chat = chat_qs.first()
        if chat is None:
            chat = Chat.objects.create(user1=user1, user2=user2)
        return chat
