from typing import Any, override

from django.conf import settings
from django.contrib.admin import ModelAdmin, site
from django.http import HttpRequest

from secret.models import (
    Bank,
    Brand,
    CardType,
    LoginCredential,
    NoteType,
    PaymentCard,
    SecurityNote,
    Service,
)


class BasesWardenModelAdmin(ModelAdmin):
    exclude: tuple[str, ...] = tuple()
    _exclude: tuple[str, ...] = tuple()

    @override
    def has_change_permission(self, r: HttpRequest, obj=None) -> bool:  # type: ignore[override]
        return False if not r.user.is_superuser else True  # type: ignore

    @override
    def get_form(self, r: HttpRequest, obj: Any = None, **kwargs: Any) -> Any:  # type: ignore[override]
        if not r.user.is_superuser:  # type: ignore
            self.exclude = self._exclude

        return super().get_form(r, obj, **kwargs)


class CardAdmin(BasesWardenModelAdmin):
    list_filter = ('owner__is_active', 'card_type', 'bank', 'brand')
    search_fields = (
        'slug',
        'card_type__name',
        'bank__name',
        'brand__name',
        'owner__username',
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
        'service__name',
        'owner__username',
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
    )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'note_type', 'slug', 'created', 'updated')
    _exclude = ('owner', 'content')


class NoteTypeAdmin(BasesWardenModelAdmin):
    search_fields = ('name',)
    list_display = ('pk', 'name', 'created', 'updated')


class CardTypeAdmin(BasesWardenModelAdmin):
    search_fields = ('name',)
    list_display = ('pk', 'name', 'created', 'updated')


class BankAdmin(BasesWardenModelAdmin):
    search_fields = ('name',)
    list_display = ('pk', 'name', 'created', 'updated')


class BrandAdmin(BasesWardenModelAdmin):
    search_fields = ('name',)
    list_display = ('pk', 'name', 'created', 'updated')


class ServiceAdmin(BasesWardenModelAdmin):
    search_fields = ('name',)
    list_display = ('pk', 'name', 'created', 'updated')


if settings.IS_DEV_ENVIRONMENT:
    site.register(PaymentCard, CardAdmin)
    site.register(LoginCredential, LoginCredentialAdmin)
    site.register(SecurityNote, SecurityNoteAdmin)


site.register(NoteType, NoteTypeAdmin)
site.register(CardType, CardTypeAdmin)
site.register(Bank, BankAdmin)
site.register(Brand, BrandAdmin)
site.register(Service, ServiceAdmin)
