from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from secret.models import Card, LoginCredential, SecurityNote


# Create your views here.
def index(r: HttpRequest) -> HttpResponse:
    if r.user.is_authenticated:
        credentials: LoginCredential = r.user.credentials.all()
        cards: Card = r.user.cards.all()
        notes: SecurityNote = r.user.notes.all()

        return render(
            r,
            "home/index.html",
            {
                "credentials": credentials[:4],
                "cards": cards[:4],
                "notes": notes[:4],
                "credentials_count": credentials.count(),
                "cards_count": cards.count(),
                "notes_count": notes.count(),
            },
        )

    return render(r, "home/landing.html")
