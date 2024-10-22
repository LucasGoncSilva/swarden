from typing import Final, Type

from django.contrib.admin import ModelAdmin, register
from django.contrib.auth import admin as auth_admin

from account.forms import UserChangeForm, UserCreationForm
from account.models import ActivationAccountToken, User


@register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display: Final = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    search_fields: Final = ('username', 'email', 'first_name', 'last_name')
    add_fieldsets: Final = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    form: Type[UserChangeForm] = UserChangeForm
    add_form: Type[UserCreationForm] = UserCreationForm


@register(ActivationAccountToken)
class ActivationAccountTokenAdmin(ModelAdmin):
    list_filter: Final = ('user__is_active',)
