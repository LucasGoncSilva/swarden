from django.conf import settings
from django.contrib.admin import ModelAdmin, site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import UserChangeForm, UserCreationForm
from account.models import ActivationAccountToken, RecoveryPhrase, User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_active', 'is_staff', 'created')
    search_fields = ('username',)

    readonly_fields = ('created',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        ('Important dates', {'fields': ('last_login', 'created')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            },
        ),
    )

    ordering = ('username',)


class ActivationAccountTokenAdmin(ModelAdmin):
    list_display = ('user__username', 'value', 'used')
    list_filter = ('user__is_active',)


class RecoveryPhraseAdmin(ModelAdmin):
    list_display = ('user__username', 'fingerprint', 'is_active')
    readonly_fields = ('phrase_hash', 'fingerprint')


if settings.IS_DEV_ENVIRONMENT:
    site.register(User, UserAdmin)
    site.register(ActivationAccountToken, ActivationAccountTokenAdmin)
    site.register(RecoveryPhrase, RecoveryPhraseAdmin)
