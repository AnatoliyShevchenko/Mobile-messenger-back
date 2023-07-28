# Rest Framework
from rest_framework import serializers

# Local
from .models import (
    ChatRoom, 
    Messages,
)
from auths.serializers import ClientSerializer


class CustomDateTimeField(serializers.DateTimeField):
    """Serializer for view time created message."""

    def to_representation(self, value):
        if value is not None:
            return value.strftime('%d-%m-%Y %H:%M:%S')
        return None
    

class ChatsSerializer(serializers.ModelSerializer):
    """Serializer for view all chats."""

    class Meta:
        model = ChatRoom
        fields = (
            'id',
            'title'
        )


class ChatMessagesSerializer(serializers.ModelSerializer):
    """Serializer for view messages in chat."""

    sender = ClientSerializer()
    created_at = CustomDateTimeField()

    class Meta:
        model = Messages
        fields = (
            'id',
            'sender',
            'content',
            'image',
            'created_at'
        )

        