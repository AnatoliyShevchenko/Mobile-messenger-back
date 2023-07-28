# Django
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Local
from auths.models import Client
from .utils import read_keys_from_file

# Third-Party
import rsa
from typing import Any
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


private_path = settings.PRIVATE_PATH
public_path = settings.PUBLIC_PATH


class ChatRoom(models.Model):
    """Class for chats."""

    title = models.CharField(
        verbose_name='название',
        max_length=250,
        unique=True,
    )
    members = ArrayField(
        models.IntegerField(),
        blank=True,
        default=list
    )
    created_at = models.DateTimeField(
        verbose_name='создан',
        auto_now_add=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = ('чат')
        verbose_name_plural = ('чаты')

    def __str__(self) -> str:
        return f'{self.title} | {self.created_at}'
    

class MessageManager(models.Manager):
    """Manager for messages."""

    def encrypt_message(
        self,
        message: str, 
    ) -> str:
        key = read_keys_from_file(public_path)
        public_key_str = key.strip()
        public_key = rsa.PublicKey.load_pkcs1(
            public_key_str.encode('utf-8')
        )
        encrypted_message = rsa.encrypt(
            message.encode('utf-8'), 
            public_key
        )
        encoded_message = encrypted_message.hex()
        return encoded_message

    def decrypt_message(
        self,
        message: str, 
    ) -> str:
        key = read_keys_from_file(private_path)
        private_key_str = key.strip()
        private_key = rsa.PrivateKey.load_pkcs1(
            private_key_str.encode('utf-8')
            )
        encrypted_message = bytes.fromhex(message)
        decrypted_message = rsa.decrypt(
            encrypted_message, 
            private_key
        )
        return decrypted_message.decode('utf-8')
    
    def send_message(
        self, 
        sender: Client, 
        chat: ChatRoom, 
        content: str = None,
        image: Any = None
    ):
        if content:
            message = self.create(
                sender=sender,
                chat=chat,
                content=self.encrypt_message(content),
                sent=True
            )
            channel_layer = get_channel_layer()
            room_group_name = f'chat_{chat.id}'
            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {
                    'type': 'chat.message',
                    'sender': {
                        "username" : sender.username
                    },
                    'content': content,
                }
            )
        if image:
            message = self.create(
                sender=sender,
                chat=chat,
                image=image,
                sent=True
            )
        return message
    

class Messages(models.Model):
    """Class for chat between users."""

    chat = models.ForeignKey(
        to=ChatRoom,
        on_delete=models.CASCADE,
        verbose_name='чат'
    )
    sender = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name='sender_messages',
        verbose_name='отправитель'
    )
    content = models.TextField(
        verbose_name='сообщение',
        max_length=500,
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name='картинка',
        upload_to='chats/images',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    sent = models.BooleanField(
        verbose_name='отправлено',
        default=False
    )
    delivered = models.BooleanField(
        verbose_name='доставлено',
        null=True
    )
    readed = models.BooleanField(
        verbose_name='прочитано',
        default=False
    )

    objects = MessageManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self) -> str:
        return f"{self.sender} в чате {self.chat}"
    
