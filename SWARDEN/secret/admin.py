from typing import Any

from django.http import HttpRequest
from django.contrib import admin

from .models import Card, LoginCredential, SecurityNote


# Register your models here.
class BasesWardenModelAdmin(admin.ModelAdmin):
    exclude = tuple()
    _exclude = tuple()

    def has_change_permission(self, r: HttpRequest, obj=None):
        return False if not r.user.is_superuser else True

    def get_form(self, request: HttpRequest, obj: Any = None, **kwargs: Any):
        if not request.user.is_superuser:
            self.exclude = self._exclude

        return super().get_form(request, obj, **kwargs)


@admin.register(Card)
class CardAdmin(BasesWardenModelAdmin):
    prepopulated_fields = {'slug': ('bank', 'name')}
    list_display = ('pk', 'slug', 'created', 'updated')
    _exclude = (
        'owner',
        'card_type',
        'number',
        'expiration',
        'cvv',
        'brand',
        'owners_name',
        'note',
    )


@admin.register(LoginCredential)
class LoginCredentialAdmin(BasesWardenModelAdmin):
    prepopulated_fields = {'slug': ('service', 'name')}
    list_display = ('pk', 'slug', 'created', 'updated')
    _exclude = (
        'owner',
        'thirdy_party_login',
        'thirdy_party_login_name',
        'login',
        'password',
        'note',
    )


@admin.register(SecurityNote)
class SecurityNoteAdmin(BasesWardenModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'slug', 'created', 'updated')
    _exclude = ('owner', 'content')
