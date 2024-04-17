from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Create your models here


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


def validate_image_type(value):
    if not value.name.endswith('.jpeg') and not value.name.endswith('.jpg') and not value.name.endswith('png'):
        raise ValidationError(
            _("Invalid image type. ONly JPG, JPEG and PNG formats are allowed"))


def validate_image_size(value):
    max_size = 10 * 1024
    if value.size > max_size:
        raise ValidationError(
            _("The file size exceeds the maximun allowed size of 10MB"))


def validate_file_type(value):
    if not value.name.endswith('.pdf') and not value.name.endswith('.docs') and not value.name.endswith('docx') and not value.name.endswith('doc'):
        raise ValidationError(
            _("Invalid image type. ONly PDF, DOCS, DOCX, DOC formats are allowed"))


def validate_file_size(value):
    max_size = 34 * 1024
    if value.size > max_size:
        raise ValidationError(
            _("The file size exceeds the maximun allowed size of 34MB"))


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages")
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages_from_me')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_to_me")
    content = models.CharField(max_length=512)
    # storage=MediaCloudinaryStorage())
    image = models.ImageField(
        upload_to='chats/message/image', null=True, blank=True, validators=[validate_image_type, validate_image_size])
    # storage=RawMediaCloudinaryStorage())
    file_message = models.FileField(
        upload_to='chats/message/file', null=True, blank=True, validators=[validate_file_type, validate_file_size])
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}\
            {self.content} [{self.timestamp}]"


class NotificationFromAdmin(models.Model):
    content = models.CharField(max_length=512)
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_messages_to_me"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class ChatParticipantsChannel(models.Model):
    channel = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.channel)


class ChatRoom(models.Model):
    name = models.CharField(max_length=256)
    last_message = models.CharField(max_length=1024, null=True)
    last_sent_user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class Messages(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='messages_chat')
    content = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class ChatRoomParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
