from typing import Final

from django.urls import path, URLPattern

from account.views import (
    register_view,
    activate_account,
    login_view,
    logout_view,
    activate_account_missing_parameter,
)


app_name: Final[str] = "account"

urlpatterns: list[URLPattern] = [
    path("registrar", register_view, name="register"),
    path("ativar/", activate_account_missing_parameter, name="activate_no_parameter"),
    path(
        "ativar/<uidb64>/", activate_account_missing_parameter, name="activate_no_token"
    ),
    path("ativar/<uidb64>/<token>", activate_account, name="activate"),
    path("entrar", login_view, name="login"),
    path("sair", logout_view, name="logout"),
]
