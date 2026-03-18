from os import getenv
from typing import Final

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path


urlpatterns: list[URLResolver | URLPattern] = [
    # System functionality's pages
    path(f'{getenv("ADMIN", "admin")}/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('error/', include('err.urls')),
    # User's pages
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('secrets/', include('secret.urls')),
    path('plans/', include('plans.urls')),
]

if settings.IS_DEV_ENVIRONMENT and settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

handler403: Final[str] = 'err.views.handle403'
handler404: Final[str] = 'err.views.handle404'
handler429: Final[str] = 'err.views.handle429'
handler500: Final[str] = 'err.views.handle500'
