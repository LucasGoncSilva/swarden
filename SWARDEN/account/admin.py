from typing import Final

from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from account.models import User, ActivationAccountToken
from account.forms import UserChangeForm, UserCreationForm


# Register your models here.
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    add_fieldsets: Final = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm


admin.site.register(ActivationAccountToken)
