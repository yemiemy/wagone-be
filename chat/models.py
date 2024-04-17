from django.db import models
from accounts.models import User
from core.utils import get_uuid

# Create your models here.


class Chat(models.Model):
    id = models.UUIDField(
        primary_key=True, default=get_uuid, editable=False
    )  # type: ignore
    user1 = models.ForeignKey(
        User, related_name="chats_as_user1", on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User, related_name="chats_as_user2", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user1",
            "user2",
        )
        ordering = ("-created_at",)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=get_uuid, editable=False
    )  # type: ignore
    sender = models.ForeignKey(
        User, related_name="messages_sent", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="messages_received", on_delete=models.CASCADE
    )
    chat = models.ForeignKey(
        Chat, related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
