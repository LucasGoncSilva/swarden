from typing import Final

from django.urls import URLPattern, path

from account.views import (
    activate_account,
    activate_account_missing_parameter,
    login_view,
    logout_view,
    register_view,
)


app_name: Final[str] = 'account'

urlpatterns: list[URLPattern] = [
    path('registrar', register_view, name='register'),
    path('ativar/', activate_account_missing_parameter, name='activate_no_parameter'),
    path(
        'ativar/<uidb64>/', activate_account_missing_parameter, name='activate_no_token'
    ),
    path('ativar/<uidb64>/<token>', activate_account, name='activate'),
    path('entrar', login_view, name='login'),
    path('sair', logout_view, name='logout'),
]
