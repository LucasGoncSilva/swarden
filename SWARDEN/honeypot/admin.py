from typing import Final

from django.contrib import admin

from .models import Attempt


# Register your models here.
@admin.register(Attempt)
class AttempAdmin(admin.ModelAdmin):
    readonly_fields: Final = ('IP', 'username', 'password', 'URL', 'timestamp')
