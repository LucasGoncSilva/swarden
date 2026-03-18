from asyncio import iscoroutine
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from datetime import datetime
from inspect import iscoroutinefunction
from logging import ERROR, INFO, Logger, getLogger
from os import getenv
from socket import gethostname
from time import perf_counter
from typing import Any, TypedDict, cast
from uuid import UUID

from asgiref.sync import markcoroutinefunction, sync_to_async
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.utils import timezone
from django.utils.decorators import sync_and_async_middleware


type ResponseHandler = Callable[
    [HttpRequest], HttpResponse | Awaitable[HttpResponseBase]
]


class RequestContext(TypedDict):
    http_method: str
    is_async: bool
    http_method: str
    path: str
    status_code: int
    duration_ms: float
    timestamp: str
    user_agent: str
    content_type: str
    response_bytesize: int


class UserContext(TypedDict):
    user_id: UUID
    session_id: str
    country: str
    locale: str
    timezone: str


class InfraContext(TypedDict):
    server: str
    region: str
    git_sha: str


class ErrorContext(TypedDict):
    stacktrace: str | None


class BasicLoggerData(TypedDict):
    request_context: RequestContext
    user_context: UserContext
    infra_context: InfraContext
    error_context: ErrorContext


LOGGER: Logger = getLogger('wide_events')
_LOG_CONTEXT: ContextVar[dict[str, Any]] = ContextVar('log_context', default={})

SERVER_NAME: str = gethostname()
SERVER_REGION: str = getenv('SERVER_REGION', 'unknown')
ENVIRONMENT: str = getenv('ENV_NAME', 'dev')
GIT_SHA: str = getenv('GIT_SHA', 'unknown')


def get_log_context() -> dict[str, Any]:
    return _LOG_CONTEXT.get()


def bind_log_data_middleware(**kwargs: Any) -> None:
    get_log_context().update(kwargs)


def clear_log_context() -> None:
    _LOG_CONTEXT.set({})


@sync_and_async_middleware
class WideEventLoggingMiddleware:
    sync_capable: bool = True
    async_capable: bool = True

    def __init__(self, get_response: ResponseHandler) -> None:
        self.get_response: ResponseHandler = get_response
        self._is_async: bool = iscoroutinefunction(self.get_response)

        if self._is_async:
            markcoroutinefunction(self)  # type: ignore

    def __call__(
        self, r: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if settings.IS_LOG_ON:
            if self._is_async:
                return self.__acall__(r)

            clear_log_context()

            start_perf: float = perf_counter()

            res = self.get_response(r)

            if iscoroutine(res):
                raise RuntimeError('Middleware received coroutine in sync mode.')

            self._emit_wide_event(r, res, start_perf, False)

            return res

        else:
            res = self.get_response(r)
            return res

    async def __acall__(self, r: HttpRequest) -> HttpResponseBase:
        if settings.IS_LOG_ON:
            clear_log_context()

            start_perf: float = perf_counter()

            res = await self.get_response(r)  # type: ignore

            await sync_to_async(self._emit_wide_event)(r, res, start_perf, True)

            return res

        else:
            res = await self.get_response(r)  # type: ignore
            return res

    def _default_request_context(
        self, r: HttpRequest, res: HttpResponse, start_perf: float, is_async: bool
    ) -> RequestContext:
        return RequestContext(
            http_method=str(r.method),
            is_async=is_async,
            path=r.path,
            status_code=res.status_code,
            duration_ms=round((perf_counter() - start_perf) * 1000, 2),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            user_agent=r.META.get('HTTP_USER_AGENT', ''),
            content_type=str(r.content_type),
            response_bytesize=len(res.content),
        )

    def _default_user_context(self, r: HttpRequest) -> UserContext:
        return UserContext(
            user_id=cast(UUID, r.user.pk),
            session_id=getattr(getattr(r, 'session', None), 'session_key', 'none')
            or 'none',
            country=r.headers.get('CF-IPCountry', 'unknown'),
            locale=getattr(r, 'LANGUAGE_CODE', 'unknown'),
            timezone=str(timezone.get_current_timezone()),
        )

    def _default_infra_context(self) -> InfraContext:
        return InfraContext(server=SERVER_NAME, region=SERVER_REGION, git_sha=GIT_SHA)

    def _default_error_context(self) -> ErrorContext:
        return ErrorContext(stacktrace=None)

    def _emit_wide_event(
        self, r: HttpRequest, res: Any, start_perf: float, is_async: bool
    ) -> None:
        request_context: RequestContext = self._default_request_context(
            r, res, start_perf, is_async
        )
        user_context: UserContext = self._default_user_context(r)
        infra_context: InfraContext = self._default_infra_context()
        error_context: ErrorContext = self._default_error_context()

        data: BasicLoggerData = BasicLoggerData(
            request_context=request_context,
            user_context=user_context,
            infra_context=infra_context,
            error_context=error_context,
        )

        bind_log_data_middleware(**data)

        context = get_log_context()

        level: int = ERROR if request_context['status_code'] >= 500 else INFO

        LOGGER.log(level, context)
