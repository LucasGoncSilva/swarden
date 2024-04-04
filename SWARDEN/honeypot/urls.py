from typing import Final

from django.urls import path, re_path, URLPattern

from honeypot.views import honeypot


app_name: Final[str] = 'honeypot'

urlpatterns: list[URLPattern] = [
    path('', honeypot, name='empty_redirect'),
    path('<path:path>', honeypot, name='redirect'),
    re_path(r'^(?P<path>.*)/$', honeypot, name='re_redirect'),
    path('login', honeypot, name='honeypot'),
]
