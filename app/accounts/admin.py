from django.contrib import admin
from .models import User, Profile
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_per_page = 25


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name',
                    'last_name', 'gender', 'country']
    list_filter = ['gender', 'country']
    search_fields = ['first_name', 'last_name', 'country']
    list_per_page = 25
    readonly_fields = ['image_view', ]

    def image_view(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url=obj.avatar.url,
            width=obj.avatar.width,
            height=obj.avatar.height
        )
        )
