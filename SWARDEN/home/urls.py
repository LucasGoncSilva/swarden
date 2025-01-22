from typing import Final

from django.urls import URLPattern, path

from home.views import index


app_name: Final[str] = 'home'

urlpatterns: list[URLPattern] = [
    path('', index, name='index'),
]
