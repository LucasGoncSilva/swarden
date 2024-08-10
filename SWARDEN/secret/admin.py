from typing import Any, Final

from django.http import HttpRequest
from django.contrib.admin import ModelAdmin, register

from secret.models import Card, LoginCredential, SecurityNote


# Register your models here.
class BasesWardenModelAdmin(ModelAdmin):
    exclude = tuple()
    _exclude = tuple()

    def has_change_permission(self, r: HttpRequest, obj=None) -> bool:
        return False if not r.user.is_superuser else True

    def get_form(self, request: HttpRequest, obj: Any = None, **kwargs: Any) -> Any:
        if not request.user.is_superuser:
            self.exclude = self._exclude

        return super().get_form(request, obj, **kwargs)


@register(Card)
class CardAdmin(BasesWardenModelAdmin):
    prepopulated_fields: Final = {"slug": ("bank", "name")}
    list_display: Final = ("pk", "slug", "created", "updated")
    _exclude: Final = (
        "owner",
        "card_type",
        "number",
        "expiration",
        "cvv",
        "brand",
        "owners_name",
        "note",
    )


@register(LoginCredential)
class LoginCredentialAdmin(BasesWardenModelAdmin):
    prepopulated_fields: Final = {"slug": ("service", "name")}
    list_display: Final = ("pk", "slug", "created", "updated")
    _exclude: Final = (
        "owner",
        "thirdy_party_login",
        "thirdy_party_login_name",
        "login",
        "password",
        "note",
    )


@register(SecurityNote)
class SecurityNoteAdmin(BasesWardenModelAdmin):
    prepopulated_fields: Final = {"slug": ("title",)}
    list_display: Final = ("pk", "slug", "created", "updated")
    _exclude: Final = ("owner", "content")
