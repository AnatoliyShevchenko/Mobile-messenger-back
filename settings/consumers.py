import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.room_name}"
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]
        sender = text_data_json["sender"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message", 
                "sender" : sender,
                "content": content
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        sender = event["sender"]
        content = event["content"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "sender" : sender,
                "content": content,
            })
        )

