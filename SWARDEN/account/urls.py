from typing import Final

from django.urls import URLPattern, path

from account.views import (
    activate_account,
    activate_account_missing_parameter,
    login,
    logout,
    recovery,
    register,
    wordlist,
)


app_name: Final[str] = 'account'

urlpatterns: list[URLPattern] = [
    path('register', register, name='register'),
    path('activate/', activate_account_missing_parameter, name='activate_no_parameter'),
    path(
        'activate/<uidb64>/',
        activate_account_missing_parameter,
        name='activate_no_token',
    ),
    path('activate/<uidb64>/<token>', activate_account, name='activate'),
    path('wordlist', wordlist, name='wordlist'),
    path('login', login, name='login'),
    path('recovery', recovery, name='recovery'),
    path('logout', logout, name='logout'),
]
