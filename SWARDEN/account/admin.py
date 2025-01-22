
from CORE.admin import swarden_admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import admin as auth_admin

from account.forms import UserChangeForm, UserCreationForm
from account.models import ActivationAccountToken, User


class UserAdmin(auth_admin.UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    add_fieldsets = (
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
    form = UserChangeForm
    add_form = UserCreationForm


class ActivationAccountTokenAdmin(ModelAdmin):
    list_filter = ('user__is_active',)


swarden_admin.register(ActivationAccountToken, ActivationAccountTokenAdmin)
swarden_admin.register(User, UserAdmin)
