# Rest Framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# SimpleJWT
from rest_framework_simplejwt.authentication import JWTAuthentication

# Django
from django.db.models import QuerySet, Q

# Third-Party
from typing import Any

# Local
from .models import (
    ChatRoom, 
    Messages,
)
from .serializers import (
    ChatsSerializer,
    ChatMessagesSerializer,
)
from abstract.mixins import ResponseMixin
from auths.models import Client


@permission_classes([IsAuthenticated])
class ChatRoomsView(APIView, ResponseMixin):
    """View for view all chats and create new."""

    authentication_classes = [JWTAuthentication]

    def get(self, request: Request) -> Response:
        """GET method for view all chats."""

        user: Client = request.user
        chats: QuerySet =\
            ChatRoom.objects.filter(members__contains=[user.id])
        if chats.exists():
            serializer: ChatsSerializer =\
                ChatsSerializer(
                    instance=chats, 
                    many=True
                )
            return self.get_response(
                key='chats',
                data=serializer.data,
                status='200'
            )

        return self.get_response(
            key='error',
            data='you have no chats at this moment',
            status='400'
        )
        
    def post(self, request: Request) -> Response:
        """POST method for create chat."""

        user: Client = request.user
        recipient: str = request.data.get('recipient')
        client: Client = Client.objects.filter(
            Q(username=recipient) |
            Q(email=recipient) |
            Q(phone_number=recipient)
        ).first()
        if client:
            chat_title = f'{user.username},{client.username}'
            ChatRoom.objects.get_or_create(
                title=chat_title,
                members=[user.id, client.id]
            )
            return self.get_response(
                key='chat',
                data='created',
                status='200'
            )
        
        return self.get_response(
            key='error',
            data='recipient not found',
            status='400'
        )
    
    def patch(self, request: Request) -> Response:
        """Join/Remove chat member."""

        user: Client = request.user
        recipient: str = request.data.get('recipient')
        chat_id: str = request.data.get('chat_id')
        action: str = request.data.get('action')
        client: QuerySet[Client] = Client.objects.filter(
            Q(username=recipient) |
            Q(email=recipient) |
            Q(phone_number=recipient)
        )
        if client.exists():
            chat: ChatRoom = ChatRoom.objects.get(id=chat_id)
            if action == 'remove':
                chat.members.remove(client.id)
                chat.title += f'{client.username}'
                chat.save(update_fields=['members', 'title'])
                message: str = f'user {client.username} has been joined'
            if action == 'join':
                chat.members.append(client.id)
                chat.title = chat.title.replace(client.username, '')
                chat.save(update_fields=['members', 'title'])
                message: str = f'user {client.username} has been removed'

            return self.get_response(
                key='success',
                data=message,
                status='200'
            )
        
        return self.get_response(
            key='error',
            data='recipient not found',
            status='400'
        )
    

@permission_classes([IsAuthenticated])
class MessagesView(APIView, ResponseMixin):
    """View for send and recieve messages."""

    authentication_classes = [JWTAuthentication]

    def get(self, request: Request, pk: str) -> Response:
        """GET method for view messages in chat."""

        chat: ChatRoom = ChatRoom.objects.get(id=pk)
        messages: QuerySet =\
            Messages.objects.filter(
                chat=chat
            ).order_by('created_at')
        if messages.exists():
            decrypted_messages: list = []
            for message in messages:
                decrypted_content: str =\
                    Messages.objects.decrypt_message(message.content)
                decrypted_message = {
                    'id': message.id,
                    'sender': message.sender,
                    'content': decrypted_content,
                    'image': message.image or None,
                    'created_at': message.created_at,
                }
                decrypted_messages.append(decrypted_message)

            serializer: ChatMessagesSerializer =\
                ChatMessagesSerializer(
                    decrypted_messages, 
                    many=True
                )
            return self.get_response(
                key='messages',
                data=serializer.data,
                status='200'
            )
        
        return self.get_response(
            key='error',
            data='you have no messages at this moment',
            status='400'
        )

    def post(self, request: Request) -> Response:
        """POST method for sending messages."""

        user: Client = request.user
        chat_id: str = request.data.get('chat_id')
        content: str = request.data.get('content')
        try:
            chat: ChatRoom = ChatRoom.objects.get(id=chat_id)

            Messages.objects.send_message(
                sender=user,
                chat=chat,
                content=content,
                # image=image
            )

            return self.get_response(
                key='success',
                data='sended',
                status='200'
            )

        except ChatRoom.DoesNotExist:
            return self.get_response(
                key='error',
                data='chat does not exist',
                status='400'
            )
    