from typing import Any

from CORE.utils import bind_log_data
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle403(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    bind_log_data(args=args, kwargs=kwargs)
    return render(
        r,
        'err/error_template.html',
        {
            'code': 403,
            'message1': 'You do not have permission to proceed.',
            'message2': 'Return to where you were or go to the homepage.',
        },
        status=403,
    )


def handle404(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    bind_log_data(args=args, kwargs=kwargs)
    return render(
        r,
        'err/error_template.html',
        {
            'code': 404,
            'message1': 'Page not found.',
            'message2': 'Return to where you were or go to the homepage.',
        },
        status=404,
    )


def handle429(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    bind_log_data(args=args, kwargs=kwargs)
    return render(
        r,
        'err/error_template.html',
        {
            'code': 429,
            'message1': 'Too many requests.',
            'message2': 'Slow down, you do not need to be this fast here.',
        },
        status=429,
    )


def handle500(r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    bind_log_data(args=args, kwargs=kwargs)
    return render(
        r,
        'err/error_template.html',
        {
            'code': 500,
            'message1': 'There was a problem with the server.',
            'message2': 'Please report the issue to the website team.',
        },
        status=500,
    )
