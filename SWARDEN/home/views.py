from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def index(r: HttpRequest) -> HttpResponse:
    if r.user.is_authenticated:
        return render(
            r,
            'home/index.html',
            {
                'credentials': r.user.credentials.all()[:4],
                'cards': r.user.cards.all()[:4],
                'notes': r.user.notes.all()[:4],
                'credentials_count': r.user.credentials.all().count(),
                'cards_count': r.user.cards.all().count(),
                'notes_count': r.user.notes.all().count(),
            },
        )

    return render(r, 'home/landing.html')
