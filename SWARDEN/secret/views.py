from collections.abc import Callable
from typing import Any, Final, Literal, override

from CORE.utils import bind_log_data
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
from django.views.generic import CreateView, DeleteView, UpdateView
from home.views import index as home_index

from secret.forms import LoginCredentialForm, PaymentCardForm, SecurityNoteForm
from secret.models import LoginCredential, PaymentCard, SecurityNote


SUCCESSFULLY_CREATED_SECRET: Final[str] = 'Secret created successfully.'
SUCCESSFULLY_UPDATED_SECRET: Final[str] = 'Secret updated successfully.'
SUCCESSFULLY_DELETED_SECRET: Final[str] = 'Secret deleted successfully.'
EMPTY_POST_MSG: Final[str] = 'Please fill the form correctly.'
SLUG_ALREADY_EXISTS_MSG: Final[str] = 'Slug already exists. Try another name or title.'
MISSING_CRITICAL_INFO: Final[str] = (
    'Missing critical information. Try again or report to the team.'
)


sensitive_post_parameters_dec: Callable = method_decorator(
    sensitive_post_parameters(), name='dispatch'
)


@sensitive_post_parameters()
@sensitive_variables()
def _list_view(
    r: HttpRequest, secret: Literal['credential', 'card', 'note']
) -> dict[str, str | list] | None:
    dispatch: dict[Literal['credential', 'card', 'note'], dict[str, list | str]] = {
        'credential': {
            'object_list': r.user.credentials.all(),  # type: ignore
            'model_name': 'Login Credentials',
        },
        'card': {
            'object_list': r.user.cards.all(),  # type: ignore
            'model_name': 'Payment Cards',
        },
        'note': {
            'object_list': r.user.notes.all(),  # type: ignore
            'model_name': 'Security Notes',
        },
    }

    return dispatch.get(secret)


@sensitive_post_parameters()
@sensitive_variables()
@login_required
def index(r: HttpRequest) -> HttpResponse:
    return home_index(r)


# Credentials views
@sensitive_post_parameters()
@sensitive_variables()
@login_required
def credential_list_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        'secret/list_view.html',
        _list_view(r, 'credential'),
    )


@sensitive_post_parameters()
@sensitive_variables()
@login_required
def credential_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
    credential: LoginCredential = get_object_or_404(
        LoginCredential, owner=r.user, slug=slug
    )

    return render(r, 'secret/Credential/detail_view.html', {'object': credential})


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class CredentialCreateView(SuccessMessageMixin, CreateView):
    model: type = LoginCredential
    template_name: str | None = 'secret/create_view.html'
    form_class = LoginCredentialForm
    success_message = SUCCESSFULLY_CREATED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Addition', 'model': 'Login Credential'})
        return ctx

    @override
    @method_decorator(sensitive_variables())
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore[override]
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        if (
            LoginCredential.objects.filter(
                owner=r.user, slug=r.POST.get('slug')
            ).count()
            > 0
        ):
            error(r, SLUG_ALREADY_EXISTS_MSG)
            bind_log_data(args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        return super().post(r, *args, **kwargs)

    @override
    def form_valid(self, form: LoginCredentialForm):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    @override
    def form_invalid(self, form: LoginCredentialForm):
        res = super().form_invalid(form)
        res.status_code = 422
        return res


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class CredentialUpdateView(SuccessMessageMixin, UpdateView):
    model: type = LoginCredential
    template_name: str | None = 'secret/create_view.html'
    form_class = LoginCredentialForm
    success_message = SUCCESSFULLY_UPDATED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Edition', 'model': 'Login Credential'})
        return ctx

    @override
    @method_decorator(sensitive_variables())
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore[override]
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        post_pk: str | None = r.POST.get('pk')

        if post_pk is None or (slug := r.POST.get('slug')) is None:
            error(r, MISSING_CRITICAL_INFO)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        filter_data: dict = dict(owner=r.user, slug=slug)

        if (
            LoginCredential.objects.filter(**filter_data).exclude(pk=post_pk).count()
            > 0
        ):
            error(r, SLUG_ALREADY_EXISTS_MSG)
            bind_log_data(args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        return super().post(r, *args, **kwargs)

    @override
    def form_invalid(self, form: LoginCredentialForm):
        res = super().form_invalid(form)
        res.status_code = 422
        return res


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class CredentialDeleteView(SuccessMessageMixin, DeleteView):
    model: type = LoginCredential
    template_name: str | None = 'secret/delete_view.html'
    success_url = '/secrets/credentials/'
    success_message = SUCCESSFULLY_DELETED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Deletion', 'model': 'Login Credential'})
        return ctx


# Cards views
@sensitive_post_parameters()
@sensitive_variables()
@login_required
def card_list_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        'secret/list_view.html',
        _list_view(r, 'card'),
    )


@sensitive_post_parameters()
@sensitive_variables()
@login_required
def card_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
    card: PaymentCard = get_object_or_404(
        PaymentCard,
        owner=r.user,
        slug=slug,
    )

    return render(r, 'secret/Card/detail_view.html', {'object': card})


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class CardCreateView(SuccessMessageMixin, CreateView):
    model: type = PaymentCard
    template_name: str | None = 'secret/create_view.html'
    form_class = PaymentCardForm
    success_message = SUCCESSFULLY_CREATED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Addition', 'model': 'Payment Card'})
        return ctx

    @override
    @method_decorator(sensitive_variables())
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore[override]
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        if (
            PaymentCard.objects.filter(owner=r.user, slug=r.POST.get('slug')).count()
            > 0
        ):
            error(r, SLUG_ALREADY_EXISTS_MSG)
            bind_log_data(args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        return super().post(r, *args, **kwargs)

    @override
    def form_valid(self, form: PaymentCardForm):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    @override
    def form_invalid(self, form: PaymentCardForm):
        res = super().form_invalid(form)
        res.status_code = 422
        return res


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class CardUpdateView(SuccessMessageMixin, UpdateView):
    model: type = PaymentCard
    template_name: str | None = 'secret/create_view.html'
    form_class = PaymentCardForm
    success_message = SUCCESSFULLY_UPDATED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Edition', 'model': 'Payment Card'})
        return ctx

    @override
    @method_decorator(sensitive_variables())
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore[override]
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        post_pk: str | None = r.POST.get('pk')

        if post_pk is None or (slug := r.POST.get('slug')) is None:
            error(r, MISSING_CRITICAL_INFO)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        filter_data: dict = dict(owner=r.user, slug=slug)

        if PaymentCard.objects.filter(**filter_data).exclude(pk=post_pk).count() > 0:
            error(r, SLUG_ALREADY_EXISTS_MSG)
            bind_log_data(args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        return super().post(r, *args, **kwargs)

    @override
    def form_invalid(self, form: PaymentCardForm):
        res = super().form_invalid(form)
        res.status_code = 422
        return res


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class CardDeleteView(SuccessMessageMixin, DeleteView):
    model: type = PaymentCard
    template_name: str | None = 'secret/delete_view.html'
    success_url = '/secrets/payment-cards/'
    success_message = SUCCESSFULLY_DELETED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Deletion', 'model': 'Payment Card'})
        return ctx


# Notes views
@sensitive_post_parameters()
@sensitive_variables()
@login_required
def note_list_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        'secret/list_view.html',
        _list_view(r, 'note'),
    )


@sensitive_post_parameters()
@sensitive_variables()
@login_required
def note_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
    note: SecurityNote = get_object_or_404(SecurityNote, owner=r.user, slug=slug)

    return render(r, 'secret/Note/detail_view.html', {'object': note})


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class NoteCreateView(SuccessMessageMixin, CreateView):
    model: type = SecurityNote
    template_name: str | None = 'secret/create_view.html'
    form_class = SecurityNoteForm
    success_message = SUCCESSFULLY_CREATED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Addition', 'model': 'Security Note'})
        return ctx

    @override
    @method_decorator(sensitive_variables())
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore[override]
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        if (
            SecurityNote.objects.filter(owner=r.user, slug=r.POST.get('slug')).count()
            > 0
        ):
            error(r, SLUG_ALREADY_EXISTS_MSG)
            bind_log_data(args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        return super().post(r, *args, **kwargs)

    @override
    def form_valid(self, form: SecurityNoteForm):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    @override
    def form_invalid(self, form: SecurityNoteForm):
        res = super().form_invalid(form)
        res.status_code = 422
        return res


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class NoteUpdateView(SuccessMessageMixin, UpdateView):
    model: type = SecurityNote
    template_name: str | None = 'secret/create_view.html'
    form_class = SecurityNoteForm
    success_message = SUCCESSFULLY_UPDATED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Edition', 'model': 'Security Note'})
        return ctx

    @override
    @method_decorator(sensitive_variables())
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  # type: ignore[override]
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        post_pk: str | None = r.POST.get('pk')

        if post_pk is None or (slug := r.POST.get('slug')) is None:
            error(r, MISSING_CRITICAL_INFO)
            bind_log_data(POST=r.POST, args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        filter_data: dict = dict(owner=r.user, slug=slug)

        if SecurityNote.objects.filter(**filter_data).exclude(pk=post_pk).count() > 0:
            error(r, SLUG_ALREADY_EXISTS_MSG)
            bind_log_data(args=args, kwargs=kwargs)
            res = super().get(r)
            res.status_code = 422
            return res

        return super().post(r, *args, **kwargs)

    @override
    def form_invalid(self, form: SecurityNoteForm):
        res = super().form_invalid(form)
        res.status_code = 422
        return res


@sensitive_post_parameters_dec
@method_decorator(login_required, name='dispatch')
class NoteDeleteView(SuccessMessageMixin, DeleteView):
    model: type = SecurityNote
    template_name: str | None = 'secret/delete_view.html'
    success_url = '/secrets/notes/'
    success_message = SUCCESSFULLY_DELETED_SECRET

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context_data(**kwargs)
        ctx.update({'action': 'Deletion', 'model': 'Security Note'})
        return ctx
