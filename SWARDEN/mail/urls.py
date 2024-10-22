from typing import Final

from django.urls import URLPattern, path

from mail.views import export_secrets, export_secrets_no_argument


app_name: Final[str] = 'mail'

urlpatterns: list[URLPattern] = [
    path(
        'exportar-segredos/',
        export_secrets_no_argument,
        name='export_secrets_no_argument',
    ),
    path(
        'exportar-segredos/<str:secret_type>',
        export_secrets,
        name='export_secrets',
    ),
]
