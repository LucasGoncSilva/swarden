from collections.abc import Callable
from typing import Any, Final, Literal

from django.contrib.auth.decorators import login_required
from django.contrib.messages import error
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView

from secret.models import Card, LoginCredential, SecurityNote


EMPTY_POST_MSG: Final[str] = 'Preencha corretamente todos os campos solicitados'
FEEDBACK_MSG: Final[str] = 'Slug já existente. Tente outro apelido ou título.'

login_dec: Callable = login_required(login_url='/conta/entrar')
login_dec_dispatch: Callable = method_decorator(login_dec, name='dispatch')


def _list_view(
    r: HttpRequest, secret: Literal['credential', 'card', 'note']
) -> dict[str, str | list] | None:
    dispatch: dict[Literal['credential', 'card', 'note'], dict[str, list | str]] = {
        'credential': {
            'object_list': r.user.credentials.all(),  # type: ignore
            'model_name': 'Credenciais',
        },
        'card': {'object_list': r.user.cards.all(), 'model_name': 'Cartões'},  # type: ignore
        'note': {'object_list': r.user.notes.all(), 'model_name': 'Anotações'},  # type: ignore
    }

    return dispatch.get(secret)


@login_dec
def index(r: HttpRequest) -> HttpResponse:
    return render(r, 'secret/index.html')


# Credentials views
@login_dec
def credential_list_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        'secret/list_view.html',
        _list_view(r, 'credential'),
    )


@login_dec
def credential_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
    credential: LoginCredential = get_object_or_404(
        LoginCredential, owner=r.user, slug=slug
    )

    return render(r, 'secret/Credential/detail_view.html', {'object': credential})


@login_dec_dispatch
class CredentialCreateView(CreateView):
    model: type = LoginCredential
    template_name: str = 'secret/create_view.html'
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adição'
        context['model'] = 'Credencial'
        return context

    def post(
        self, r: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:credential_create_view'))

        if LoginCredential.objects.filter(
            owner=r.user, slug=r.POST.get('slug')
        ).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)

        return super().post(r, *args, **kwargs)


@login_dec_dispatch
class CredentialUpdateView(UpdateView):
    model: type = LoginCredential
    template_name: str = 'secret/create_view.html'
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edição'
        context['model'] = 'Credencial'
        return context

    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))

        if LoginCredential.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)

        return super().post(r, *args, **kwargs)


@login_dec_dispatch
class CredentialDeleteView(DeleteView):
    model: type = LoginCredential
    template_name: str = 'secret/delete_view.html'
    success_url = '/segredos/credenciais'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Exclusão'
        context['model'] = 'Credencial'
        return context


# Cards views
@login_dec
def card_list_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        'secret/list_view.html',
        _list_view(r, 'card'),
    )


@login_dec
def card_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
    card: Card = get_object_or_404(Card, owner=r.user, slug=slug)

    return render(r, 'secret/Card/detail_view.html', {'object': card})


@login_dec_dispatch
class CardCreateView(CreateView):
    model: type = Card
    template_name: str = 'secret/create_view.html'
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adição'
        context['model'] = 'Cartão'
        return context

    def post(
        self, r: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:card_create_view'))

        if Card.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)

        return super().post(r, *args, **kwargs)


@login_dec_dispatch
class CardUpdateView(UpdateView):
    model: type = Card
    template_name: str = 'secret/create_view.html'
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edição'
        context['model'] = 'Cartão'
        return context

    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))

        if Card.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)

        return super().post(r, *args, **kwargs)


@login_dec_dispatch
class CardDeleteView(DeleteView):
    model: type = Card
    template_name: str = 'secret/delete_view.html'
    success_url = '/segredos/cartoes'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Exclusão'
        context['model'] = 'Cartão'
        return context


# Security Notes views
@login_dec
def note_list_view(r: HttpRequest) -> HttpResponse:
    return render(
        r,
        'secret/list_view.html',
        _list_view(r, 'note'),
    )


@login_dec
def note_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
    note: SecurityNote = get_object_or_404(SecurityNote, owner=r.user, slug=slug)

    return render(r, 'secret/Note/detail_view.html', {'object': note})


@login_dec_dispatch
class NoteCreateView(CreateView):
    model: type = SecurityNote
    template_name: str = 'secret/create_view.html'
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adição'
        context['model'] = 'Anotação'
        return context

    def post(
        self, r: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:note_create_view'))

        if SecurityNote.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)

        return super().post(r, *args, **kwargs)


@login_dec_dispatch
class NoteUpdateView(UpdateView):
    model: type = SecurityNote
    template_name: str = 'secret/create_view.html'
    fields = '__all__'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edição'
        context['model'] = 'Anotação'
        return context

    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))

        if SecurityNote.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)

        return super().post(r, *args, **kwargs)


@login_dec_dispatch
class NoteDeleteView(DeleteView):
    model: type = SecurityNote
    template_name: str = 'secret/delete_view.html'
    success_url = '/segredos/anotacoes'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Exclusão'
        context['model'] = 'Anotação'
        return context
