from typing import Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from utils import get_ip_address
from .models import Attempt


# Create your views here.
def honeypot(r: HttpRequest, path: str | None = None) -> HttpResponse:
    if r.method == 'POST':
        ip: Any | None = get_ip_address(r)

        username: str | None = r.POST.get('username')
        password: str | None = r.POST.get('password')
        url: str = r.get_full_path().split('=')[1]

        Attempt.objects.create(IP=ip, username=username, password=password, url=url)

        return render(r, 'honeypot/loop.html', {'next': url})

    return render(r, 'honeypot/honeypot.html', {'next': r.path})
