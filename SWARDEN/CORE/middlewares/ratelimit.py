from asyncio import to_thread
from collections.abc import Awaitable, Callable
from inspect import iscoroutinefunction
from os import getenv
from typing import Final

from asgiref.sync import markcoroutinefunction
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import sync_and_async_middleware
from django_smart_ratelimit import ratelimit


@sync_and_async_middleware
class RateLimitMiddleware:
    ERR_CODE: Final[int] = 429
    EXEMPT_URLS: Final[list[str]] = [
        settings.STATIC_URL,
        f'/{getenv("ADMIN", "admin")}/',
        f'/{getenv("ADMIN", "admin")}/jsi18n',
        reverse('err:403'),
        reverse('err:404'),
        reverse('err:429'),
        reverse('err:500'),
    ]

    def __init__(
        self,
        get_response: Callable[
            [HttpRequest], HttpResponseBase | Awaitable[HttpResponseBase]
        ],
    ) -> None:
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)

        if self.async_mode:
            markcoroutinefunction(self)  # type: ignore

    def __call__(
        self, r: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self.async_mode:
            return self.__acall__(r)

        check = self._check_rate_limit(r)
        if check:
            return check

        res = self.get_response(r)

        return self._handle_response(r, res)  # type: ignore

    async def __acall__(self, r: HttpRequest) -> HttpResponseBase:
        check = await to_thread(self._check_rate_limit, r)
        if check:
            return check

        res = await self.get_response(r)  # type: ignore

        if any(r.path.startswith(url) for url in self.EXEMPT_URLS):
            return res

        if res.status_code == self.ERR_CODE:
            return await to_thread(self._render_error, r)

        return res

    def _check_rate_limit(self, r: HttpRequest) -> HttpResponse | None:
        if not settings.RATELIMIT_ENABLE:
            return None

        if any(r.path.startswith(url) for url in self.EXEMPT_URLS):
            return None

        @ratelimit(
            key='ip',
            rate=settings.RATELIMIT_DEFAULT_LIMIT,
            algorithm=settings.RATELIMIT_ALGORITHM,
        )
        def _wrapped_check(request: HttpRequest) -> None:
            return None

        response = _wrapped_check(r)

        if isinstance(response, HttpResponse) and response.status_code == self.ERR_CODE:
            return self._render_error(r)

        return response

    def _handle_response(
        self, r: HttpRequest, res: HttpResponseBase
    ) -> HttpResponseBase:
        if any(r.path.startswith(url) for url in self.EXEMPT_URLS):
            return res

        if res.status_code == self.ERR_CODE:
            return self._render_error(r)
        return res

    def _render_error(self, r: HttpRequest) -> HttpResponse:
        return render(
            r,
            'err/error_template.html',
            {
                'code': 429,
                'message1': 'Too many requests.',
                'message2': 'Slow down, you do not need to be this fast here.',
            },
            status=self.ERR_CODE,
        )
