from os import getenv
from typing import Final

from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import URLPattern, URLResolver, include, path

from CORE.admin import swarden_admin


urlpatterns: list[URLResolver | URLPattern] = [
    # Adm pages
    path('admin/', include('honeypot.urls')),
    # System functionality's pages
    path('account/', include('account.urls')),
    path(
        'reset',
        PasswordResetView.as_view(template_name='account/password_reset.html'),
        name='password_reset',
    ),
    path(
        'reset-sent',
        PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(
            template_name='account/password_reset_confirm.html'
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset-complete',
        PasswordResetCompleteView.as_view(
            template_name='account/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path('captcha/', include('captcha.urls')),
    path('send-email/', include('mail.urls')),
    path('error/', include('err.urls')),
    # User's pages
    path('', include('home.urls')),
    path('secrets/', include('secret.urls')),
    path('general/', include('general.urls')),
    path('plans/', include('plans.urls')),
]

if getenv('DJANGO_SETTINGS_MODULE', 'CORE.settings.dev') == 'CORE.settings.dev':
    urlpatterns += [path(f'{getenv("ADMIN", "__manager__")}/', swarden_admin.urls)]

handler403: Final[str] = 'err.views.handle403'
handler404: Final[str] = 'err.views.handle404'
handler500: Final[str] = 'err.views.handle500'
