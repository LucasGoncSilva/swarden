from typing import Final

from django.urls import path, URLPattern

from home.views import index


app_name: Final[str] = 'home'

urlpatterns: list[URLPattern] = [
    path('', index, name='index'),
]
