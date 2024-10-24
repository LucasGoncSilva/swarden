from typing import Final

from CORE.admin import swarden_admin
from django.contrib import admin

from honeypot.models import Attempt


# @admin.register(Attempt)
class AttempAdmin(admin.ModelAdmin):
    readonly_fields: Final = ('IP', 'username', 'password', 'URL', 'timestamp')


swarden_admin.register(Attempt, AttempAdmin)
