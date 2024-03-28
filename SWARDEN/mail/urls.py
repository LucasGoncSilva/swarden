from django.urls import path, URLPattern

from . import views


app_name = 'mail'

urlpatterns: list[URLPattern] = [
    path(
        'exportar-segredos/<str:secret_type>',
        views.export_secrets,
        name='export_secrets',
    ),
]
