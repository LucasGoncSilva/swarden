from collections.abc import Callable
from typing import Final, Literal, NamedTuple

from django.urls import URLPattern, path

from secret import views as v


app_name: Final[str] = 'secret'


class SecretCRUDRoutes(NamedTuple):
    list: Callable
    create: Callable
    read: Callable
    update: Callable
    delete: Callable


def secret_crud_patterns(
    prefix: Literal['credentials', 'payment-cards', 'notes'],
    routes: SecretCRUDRoutes,
    resource_name: Literal['credential', 'card', 'note'],
) -> list:
    return [
        path(
            f'{prefix}/',
            routes.list,
            name=f'{resource_name}_list_view',
        ),
        path(
            f'{prefix}/new',
            routes.create,
            name=f'{resource_name}_create_view',
        ),
        path(
            f'{prefix}/<slug:slug>',
            routes.read,
            name=f'{resource_name}_detail_view',
        ),
        path(
            f'{prefix}/<slug:slug>/edit',
            routes.update,
            name=f'{resource_name}_update_view',
        ),
        path(
            f'{prefix}/<slug:slug>/delete',
            routes.delete,
            name=f'{resource_name}_delete_view',
        ),
    ]


urlpatterns: list[URLPattern] = [
    path('', v.index, name='index'),
    # Login Credentials views
    *secret_crud_patterns(
        'credentials',
        SecretCRUDRoutes(
            list=v.credential_list_view,
            create=v.CredentialCreateView.as_view(),
            read=v.credential_detail_view,
            update=v.CredentialUpdateView.as_view(),
            delete=v.CredentialDeleteView.as_view(),
        ),
        'credential',
    ),
    # Payment Cards views
    *secret_crud_patterns(
        'payment-cards',
        SecretCRUDRoutes(
            list=v.card_list_view,
            create=v.CardCreateView.as_view(),
            read=v.card_detail_view,
            update=v.CardUpdateView.as_view(),
            delete=v.CardDeleteView.as_view(),
        ),
        'card',
    ),
    # Security Notes views
    *secret_crud_patterns(
        'notes',
        SecretCRUDRoutes(
            list=v.note_list_view,
            create=v.NoteCreateView.as_view(),
            read=v.note_detail_view,
            update=v.NoteUpdateView.as_view(),
            delete=v.NoteDeleteView.as_view(),
        ),
        'note',
    ),
]
