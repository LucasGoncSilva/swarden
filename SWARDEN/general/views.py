from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse


# Create your views here.
@login_required(login_url='/conta/entrar')
def index(r: HttpRequest) -> HttpResponse:
    return render(r, 'general/index.html')
