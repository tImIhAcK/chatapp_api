from django.contrib import admin
from .models import Conversation, Message, ChatRoomParticipants, Messages, ChatRoom, ChatParticipantsChannel

# Register your models here.
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ChatParticipantsChannel)
admin.site.register(ChatRoom)
admin.site.register(Messages)
admin.site.register(ChatRoomParticipants)
