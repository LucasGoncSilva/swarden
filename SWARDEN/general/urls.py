from typing import Final

from django.urls import path, URLPattern

from . import views as v


app_name: Final[str] = 'general'

urlpatterns: list[URLPattern] = [
    path('', v.index, name='index'),
]
