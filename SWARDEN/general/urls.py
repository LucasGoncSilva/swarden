from typing import Final

from django.urls import path, URLPattern

from general.views import index


app_name: Final[str] = "general"

urlpatterns: list[URLPattern] = [
    path("", index, name="index"),
]
