
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from secret.models import Card, LoginCredential, SecurityNote


def index(r: HttpRequest) -> HttpResponse:
    if r.user.is_authenticated:
        credentials: LoginCredential = r.user.credentials.all()  # type: ignore
        cards: Card = r.user.cards.all()  # type: ignore
        notes: SecurityNote = r.user.notes.all()  # type: ignore

        return render(
            r,
            'home/index.html',
            {
                'credentials': credentials[:4],  # type: ignore
                'cards': cards[:4],  # type: ignore
                'notes': notes[:4],  # type: ignore
                'credentials_count': credentials.count(),  # type: ignore
                'cards_count': cards.count(),  # type: ignore
                'notes_count': notes.count(),  # type: ignore
            },
        )

    return render(r, 'home/landing.html')
