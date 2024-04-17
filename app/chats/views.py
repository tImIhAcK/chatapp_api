from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (ListModelMixin, RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet
from .models import (Conversation, Message)
from .serializers import (ConversationSerializer, MessageSerializer)
from .paginaters import MessagePagination

# Create your views here.


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.username
        )
        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_name = self.request.GET.get('conversation')
        queryset = (
            Message.objects.filter(
                conversation__name__icontains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset
