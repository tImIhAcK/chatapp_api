from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin, UserManager, AbstractUser)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        help_text=_('Required'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

    class Meta:
        ordering = ['username',]


def validate_image_type(value):
    if not value.name.endswith('.jpeg') and not value.name.endswith('.jpg') and not value.name.endswith('png'):
        raise ValidationError(
            _("Invalid image type. ONly JPG, JPEG and PNG formats are allowed"))


def validate_image_size(value):
    max_size = 10 * 1024
    if value.size > max_size:
        raise ValidationError(
            _("The file size exceeds the maximun allowed size of 10MB"))


class Profile(models.Model):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    gender = models.CharField(
        choices=GENDER, max_length=10, blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='profile_pics/', blank=True,
                               validators=[validate_image_type,
                                           validate_image_size]
                               )
    bio = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.first_name}_{self.last_name}'

    class Meta:
        ordering = ['first_name',]
