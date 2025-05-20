from CORE.admin import swarden_admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import admin as auth_admin

from account.forms import UserChangeForm, UserCreationForm
from account.models import ActivationAccountToken, User


class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (
            'Permissões',
            {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'username', 'password1', 'password2'),
            },
        ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)


class ActivationAccountTokenAdmin(ModelAdmin):
    list_filter = ('user__is_active',)


swarden_admin.register(ActivationAccountToken, ActivationAccountTokenAdmin)
swarden_admin.register(User, UserAdmin)
