from typing import Any

from CORE.admin import swarden_admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest

from secret.models import Card, LoginCredential, SecurityNote


class BasesWardenModelAdmin(ModelAdmin):
    exclude: tuple = tuple()
    _exclude: tuple = tuple()

    def has_change_permission(self, r: HttpRequest, obj=None) -> bool:  # type: ignore
        return False if not r.user.is_superuser else True  # type: ignore

    def get_form(self, request: HttpRequest, obj: Any = None, **kwargs: Any) -> Any:  # type: ignore
        if not request.user.is_superuser:  # type: ignore
            self.exclude = self._exclude  # type: ignore

        return super().get_form(request, obj, **kwargs)


class CardAdmin(BasesWardenModelAdmin):
    list_filter = ('owner__is_active', 'card_type', 'bank', 'brand')
    search_fields = (
        'card_type',
        'bank',
        'brand',
        'owner__username',
        'owner__first_name',
        'owner__last_name',
    )
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


class LoginCredentialAdmin(BasesWardenModelAdmin):
    list_filter = ('owner__is_active', 'third_party_login', 'service')
    search_fields = (
        'slug',
        'serviceowner__username',
        'owner__first_name',
        'owner__last_name',
    )
    prepopulated_fields = {'slug': ('service', 'name')}
    list_display = ('pk', 'slug', 'created', 'updated')
    _exclude = (
        'owner',
        'third_party_login',
        'third_party_login_name',
        'login',
        'password',
        'note',
    )


class SecurityNoteAdmin(BasesWardenModelAdmin):
    list_filter = ('owner__is_active', 'note_type')
    search_fields = (
        'slug',
        'owner__username',
        'owner__first_name',
        'owner__last_name',
    )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'note_type', 'slug', 'created', 'updated')
    _exclude = ('owner', 'content')


swarden_admin.register(Card, CardAdmin)
swarden_admin.register(LoginCredential, LoginCredentialAdmin)
swarden_admin.register(SecurityNote, SecurityNoteAdmin)
