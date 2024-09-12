from typing import Final, Type

from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from account.forms import UserChangeForm, UserCreationForm
from account.models import ActivationAccountToken, User


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
    form: Type[UserChangeForm] = UserChangeForm
    add_form: Type[UserCreationForm] = UserCreationForm


admin.site.register(ActivationAccountToken)
