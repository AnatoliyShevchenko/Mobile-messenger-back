# Django
from django.contrib import admin

# Local
from .models import (
    ChatRoom, 
    Messages,
)


class ChatRoomAdmin(admin.ModelAdmin):
    """Admin panel for chats."""

    model = ChatRoom
    list_display = (
        'title',
        'members',
        'created_at'
    )
    search_fields = (
        'title',
        'members'
    )
    readonly_fields = (
        'title',
        'members',
        'created_at'
    )


class MessagesAdmin(admin.ModelAdmin):
    """Admin panel for messages."""

    model = Messages
    list_display = (
        'chat',
        'sender',
        'created_at'
    )
    search_fields = (
        'chat',
        'sender',
        'created_at'
    )


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Messages, MessagesAdmin)

