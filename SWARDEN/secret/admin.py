from typing import Any, Final

from CORE.admin import swarden_admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest

from secret.models import Card, LoginCredential, SecurityNote


class BasesWardenModelAdmin(ModelAdmin):
    exclude: tuple = tuple()
    _exclude: tuple = tuple()

    def has_change_permission(self, r: HttpRequest, obj=None) -> bool:
        return False if not r.user.is_superuser else True

    def get_form(self, request: HttpRequest, obj: Any = None, **kwargs: Any) -> Any:
        if not request.user.is_superuser:
            self.exclude = self._exclude

        return super().get_form(request, obj, **kwargs)


class CardAdmin(BasesWardenModelAdmin):
    list_filter: Final = ('owner__is_active', 'card_type', 'bank', 'brand')
    search_fields: Final = (
        'card_type',
        'bank',
        'brand',
        'owner__username',
        'owner__first_name',
        'owner__last_name',
    )
    prepopulated_fields: Final = {'slug': ('bank', 'name')}
    list_display: Final = ('pk', 'slug', 'created', 'updated')
    _exclude: Final = (
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
    list_filter: Final = ('owner__is_active', 'thirdy_party_login', 'service')
    search_fields: Final = (
        'slug',
        'service' 'owner__username',
        'owner__first_name',
        'owner__last_name',
    )
    prepopulated_fields: Final = {'slug': ('service', 'name')}
    list_display: Final = ('pk', 'slug', 'created', 'updated')
    _exclude: Final = (
        'owner',
        'thirdy_party_login',
        'thirdy_party_login_name',
        'login',
        'password',
        'note',
    )


class SecurityNoteAdmin(BasesWardenModelAdmin):
    list_filter: Final = ('owner__is_active',)
    search_fields: Final = (
        'slug',
        'owner__username',
        'owner__first_name',
        'owner__last_name',
    )
    prepopulated_fields: Final = {'slug': ('title',)}
    list_display: Final = ('pk', 'slug', 'created', 'updated')
    _exclude: Final = ('owner', 'content')


swarden_admin.register(Card, CardAdmin)
swarden_admin.register(LoginCredential, LoginCredentialAdmin)
swarden_admin.register(SecurityNote, SecurityNoteAdmin)
