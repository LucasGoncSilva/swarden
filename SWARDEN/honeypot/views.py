from typing import Any, cast

from account.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from utils import get_ip_address

from honeypot.models import Attempt


def honeypot(r: HttpRequest, path: str | None = None) -> HttpResponse:
    if r.method != 'POST':
        if r.user.is_authenticated:
            return render(
                r,
                'honeypot/authenticated.html',
                {'next': r.path, 'user': cast(User, r.user).username},
            )
        return render(r, 'honeypot/honeypot.html', {'next': r.path})

    ip: Any | None = get_ip_address(r)

    username: str | None = r.POST.get('username')
    password: str | None = r.POST.get('password')
    url: str = r.get_full_path()

    Attempt.objects.create(IP=ip, username=username, password=password, URL=url)

    if r.user.is_authenticated:
        return render(
            r,
            'honeypot/authenticated.html',
            {'next': r.path, 'user': cast(User, r.user).username},
        )

    return render(r, 'honeypot/loop.html', {'next': url})
