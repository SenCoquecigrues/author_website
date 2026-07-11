from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm
)
from .models import Member
from .forms import MemberCreationForm, MemberChangeForm


class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    # change_user_password_template = Non
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'birthday', 'discord_id')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = MemberChangeForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'is_staff', 'birthday', 'discord_id')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'birthday', 'discord_id')
    search_fields = ('username', 'email')
    ordering = ('username', 'birthday')
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Member, MemberAdmin)
