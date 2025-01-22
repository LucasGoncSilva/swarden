
# File: `views.py`
Path: `SWARDEN.secret`



---

## Imports

### `#!py import Any`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Any
    ```

### `#!py import Callable`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Callable
    ```

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import Literal`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Literal
    ```

### `#!py import Type`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Type
    ```

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import error`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import error
    ```

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import HttpResponseRedirect`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponseRedirect
    ```

### `#!py import get_object_or_404`

Path: `#!py django.shortcuts`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.shortcuts import get_object_or_404
    ```

### `#!py import render`

Path: `#!py django.shortcuts`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.shortcuts import render
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.urls import reverse
    ```

### `#!py import method_decorator`

Path: `#!py django.utils.decorators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.decorators import method_decorator
    ```

### `#!py import CreateView`

Path: `#!py django.views.generic`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.views.generic import CreateView
    ```

### `#!py import DeleteView`

Path: `#!py django.views.generic`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.views.generic import DeleteView
    ```

### `#!py import UpdateView`

Path: `#!py django.views.generic`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.views.generic import UpdateView
    ```

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import SecurityNote
    ```



---

## Consts

### `#!py EMPTY_POST_MSG`

Type: `#!py Final[str]`

Value: `#!py 'Preencha corretamente todos os campos solicitados'`

??? example "SNIPPET"

    ```py
    EMPTY_POST_MSG: Final[str] = 'Preencha corretamente todos os campos solicitados'
    ```

### `#!py FEEDBACK_MSG`

Type: `#!py Final[str]`

Value: `#!py 'Slug já existente. Tente outro apelido ou título.'`

??? example "SNIPPET"

    ```py
    FEEDBACK_MSG: Final[str] = 'Slug já existente. Tente outro apelido ou título.'
    ```



---

## Classes

### `#!py class CredentialCreateView`

Parents: `CreateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class CredentialCreateView(CreateView):
        model: Type = LoginCredential
        template_name: Final[str] = 'secret/create_view.html'
        fields: Final[str] = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Adição'
            context['model'] = 'Credencial'
            return context

        def post(self, r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
            if not len(r.POST):
                error(r, EMPTY_POST_MSG)
                return HttpResponseRedirect(reverse('secret:credential_create_view'))
            if LoginCredential.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r)
    ```

### `#!py class CredentialUpdateView`

Parents: `UpdateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class CredentialUpdateView(UpdateView):
        model: Type = LoginCredential
        template_name: Final[str] = 'secret/create_view.html'
        fields: Final[str] = '__all__'

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
    ```

### `#!py class CredentialDeleteView`

Parents: `DeleteView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class CredentialDeleteView(DeleteView):
        model: Type = LoginCredential
        template_name: Final[str] = 'secret/delete_view.html'
        success_url: Final[str] = '/segredos/credenciais'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Exclusão'
            context['model'] = 'Credencial'
            return context
    ```

### `#!py class CardCreateView`

Parents: `CreateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class CardCreateView(CreateView):
        model: Type = Card
        template_name: Final[str] = 'secret/create_view.html'
        fields: Final[str] = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Adição'
            context['model'] = 'Cartão'
            return context

        def post(self, r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
            if not len(r.POST):
                error(r, EMPTY_POST_MSG)
                return HttpResponseRedirect(reverse('secret:card_create_view'))
            if Card.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r)
    ```

### `#!py class CardUpdateView`

Parents: `UpdateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class CardUpdateView(UpdateView):
        model: Type = Card
        template_name: Final[str] = 'secret/create_view.html'
        fields: Final[str] = '__all__'

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
    ```

### `#!py class CardDeleteView`

Parents: `DeleteView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class CardDeleteView(DeleteView):
        model: Type = Card
        template_name: Final[str] = 'secret/delete_view.html'
        success_url: Final[str] = '/segredos/cartoes'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Exclusão'
            context['model'] = 'Cartão'
            return context
    ```

### `#!py class NoteCreateView`

Parents: `CreateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class NoteCreateView(CreateView):
        model: Type = SecurityNote
        template_name: Final[str] = 'secret/create_view.html'
        fields: Final[str] = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Adição'
            context['model'] = 'Anotação'
            return context

        def post(self, r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
            if not len(r.POST):
                error(r, EMPTY_POST_MSG)
                return HttpResponseRedirect(reverse('secret:note_create_view'))
            if SecurityNote.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r)
    ```

### `#!py class NoteUpdateView`

Parents: `UpdateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class NoteUpdateView(UpdateView):
        model: Type = SecurityNote
        template_name: Final[str] = 'secret/create_view.html'
        fields: Final[str] = '__all__'

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
    ```

### `#!py class NoteDeleteView`

Parents: `DeleteView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec_dispatch
    class NoteDeleteView(DeleteView):
        model: Type = SecurityNote
        template_name: Final[str] = 'secret/delete_view.html'
        success_url: Final[str] = '/segredos/anotacoes'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Exclusão'
            context['model'] = 'Anotação'
            return context
    ```



---

## Functions

### `#!py def _list_view`

Type: `#!py ...`

Return Type: `#!py dict[str, str | list] | None`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, secret: Literal['credential', 'card', 'note']`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def _list_view(r: HttpRequest, secret: Literal['credential', 'card', 'note']) -> dict[str, str | list] | None:
        dispatch: dict[Literal['credential', 'card', 'note'], dict[str, list | str]] = {'credential': {'object_list': r.user.credentials.all(), 'model_name': 'Credenciais'}, 'card': {'object_list': r.user.cards.all(), 'model_name': 'Cartões'}, 'note': {'object_list': r.user.notes.all(), 'model_name': 'Anotações'}}
        return dispatch.get(secret)
    ```

### `#!py def index`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def index(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/index.html')
    ```

### `#!py def credential_list_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def credential_list_view(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/list_view.html', _list_view(r, 'credential'))
    ```

### `#!py def credential_detail_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest, slug: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def credential_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
        credential: LoginCredential = get_object_or_404(LoginCredential, owner=r.user, slug=slug)
        return render(r, 'secret/Credential/detail_view.html', {'object': credential})
    ```

### `#!py def card_list_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def card_list_view(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/list_view.html', _list_view(r, 'card'))
    ```

### `#!py def card_detail_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest, slug: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def card_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
        card: Card = get_object_or_404(Card, owner=r.user, slug=slug)
        return render(r, 'secret/Card/detail_view.html', {'object': card})
    ```

### `#!py def note_list_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def note_list_view(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/list_view.html', _list_view(r, 'note'))
    ```

### `#!py def note_detail_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest, slug: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_dec
    def note_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
        note: SecurityNote = get_object_or_404(SecurityNote, owner=r.user, slug=slug)
        return render(r, 'secret/Note/detail_view.html', {'object': note})
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adição'
        context['model'] = 'Credencial'
        return context
    ```

### `#!py def post`

Type: `#!py ...`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def post(self, r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:credential_create_view'))
        if LoginCredential.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r)
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edição'
        context['model'] = 'Credencial'
        return context
    ```

### `#!py def post`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))
        if LoginCredential.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Exclusão'
        context['model'] = 'Credencial'
        return context
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adição'
        context['model'] = 'Cartão'
        return context
    ```

### `#!py def post`

Type: `#!py ...`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def post(self, r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:card_create_view'))
        if Card.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r)
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edição'
        context['model'] = 'Cartão'
        return context
    ```

### `#!py def post`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))
        if Card.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Exclusão'
        context['model'] = 'Cartão'
        return context
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adição'
        context['model'] = 'Anotação'
        return context
    ```

### `#!py def post`

Type: `#!py ...`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def post(self, r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:note_create_view'))
        if SecurityNote.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r)
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edição'
        context['model'] = 'Anotação'
        return context
    ```

### `#!py def post`

Type: `#!py ...`

Return Type: `#!py HttpResponse`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))
        if SecurityNote.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py ...`

Return Type: `#!py dict[str, Any]`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Exclusão'
        context['model'] = 'Anotação'
        return context
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
