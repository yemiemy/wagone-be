import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat, Message
from chat.serializers import MessageSerializer
from accounts.models import User
from core.helpers.customjsonencoder import CustomJSONEncoder


class ChatConsumer(AsyncWebsocketConsumer):

    def update_chat(self, sender_id, message: str):
        sender = User.objects.get_user(sender_id)
        chat = Chat.objects.filter(id=self.room_name).first()
        if not chat:
            return

        receiver = None
        if chat.user1.id == sender.id:
            receiver = chat.user2
        else:
            receiver = chat.user1

        Message.objects.create(
            sender=sender, receiver=receiver, chat=chat, content=message
        )
        data = MessageSerializer(
            Message.objects.filter(chat=chat), many=True
        ).data
        return json.dumps(data, cls=CustomJSONEncoder)

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]
        user_id = text_data_json["user_id"]
        messages_json = await database_sync_to_async(self.update_chat)(
            user_id, message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "messages_json": messages_json,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        messages_json = event["messages_json"]

        # Send message to WebSocket
        await self.send(text_data=messages_json)
