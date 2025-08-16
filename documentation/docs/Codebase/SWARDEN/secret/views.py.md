# File: `views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret`

No file docstring provided.

---

## Imports

### `#!py import Callable`

Path: `#!py collections.abc`

Category: native

??? example "Snippet"

    ```py
    from collections.abc import Callable
    ```

### `#!py import Any`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Any
    ```

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import Literal`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Literal
    ```

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import error`

Path: `#!py django.contrib.messages`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.messages import error
    ```

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import HttpResponsePermanentRedirect`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponsePermanentRedirect
    ```

### `#!py import HttpResponseRedirect`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponseRedirect
    ```

### `#!py import get_object_or_404`

Path: `#!py django.shortcuts`

Category: trdparty

??? example "Snippet"

    ```py
    from django.shortcuts import get_object_or_404
    ```

### `#!py import redirect`

Path: `#!py django.shortcuts`

Category: trdparty

??? example "Snippet"

    ```py
    from django.shortcuts import redirect
    ```

### `#!py import render`

Path: `#!py django.shortcuts`

Category: trdparty

??? example "Snippet"

    ```py
    from django.shortcuts import render
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: trdparty

??? example "Snippet"

    ```py
    from django.urls import reverse
    ```

### `#!py import method_decorator`

Path: `#!py django.utils.decorators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.decorators import method_decorator
    ```

### `#!py import CreateView`

Path: `#!py django.views.generic`

Category: trdparty

??? example "Snippet"

    ```py
    from django.views.generic import CreateView
    ```

### `#!py import DeleteView`

Path: `#!py django.views.generic`

Category: trdparty

??? example "Snippet"

    ```py
    from django.views.generic import DeleteView
    ```

### `#!py import UpdateView`

Path: `#!py django.views.generic`

Category: trdparty

??? example "Snippet"

    ```py
    from django.views.generic import UpdateView
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import PaymentCard`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import PaymentCard
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import SecurityNote
    ```



---

## Consts

### `#!py EMPTY_POST_MSG`

Type: `#!py Final[str]`

Value: `#!py 'Preencha corretamente todos os campos solicitados.'`

??? example "Snippet"

    ```py
    EMPTY_POST_MSG: Final[str] = 'Preencha corretamente todos os campos solicitados.'
    ```

### `#!py FEEDBACK_MSG`

Type: `#!py Final[str]`

Value: `#!py 'Slug já existente. Tente outro apelido ou título.'`

??? example "Snippet"

    ```py
    FEEDBACK_MSG: Final[str] = 'Slug já existente. Tente outro apelido ou título.'
    ```



---

## Classes

### `#!py class CredentialCreateView`

Parents: `CreateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class CredentialCreateView(CreateView):
        model: type = LoginCredential
        template_name: str = 'secret/create_view.html'
        fields = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Adition'
            context['model'] = 'Login Credential'
            return context

        def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
            if not len(r.POST):
                error(r, EMPTY_POST_MSG)
                return HttpResponseRedirect(reverse('secret:credential_create_view'))
            if LoginCredential.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r, *args, **kwargs)
    ```

### `#!py class CredentialUpdateView`

Parents: `UpdateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class CredentialUpdateView(UpdateView):
        model: type = LoginCredential
        template_name: str = 'secret/create_view.html'
        fields = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Edition'
            context['model'] = 'Login Credential'
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

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class CredentialDeleteView(DeleteView):
        model: type = LoginCredential
        template_name: str = 'secret/delete_view.html'
        success_url = '/secrets/credentials'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Deletion'
            context['model'] = 'Login Credential'
            return context
    ```

### `#!py class CardCreateView`

Parents: `CreateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class CardCreateView(CreateView):
        model: type = PaymentCard
        template_name: str = 'secret/create_view.html'
        fields = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Adition'
            context['model'] = 'Payment Card'
            return context

        def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
            if not len(r.POST):
                error(r, EMPTY_POST_MSG)
                return HttpResponseRedirect(reverse('secret:card_create_view'))
            if PaymentCard.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r, *args, **kwargs)
    ```

### `#!py class CardUpdateView`

Parents: `UpdateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class CardUpdateView(UpdateView):
        model: type = PaymentCard
        template_name: str = 'secret/create_view.html'
        fields = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Edition'
            context['model'] = 'Payment Card'
            return context

        def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            post_pk: str | None = r.POST.get('pk')
            filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))
            if PaymentCard.objects.filter(**filter).exclude(pk=post_pk).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r, *args, **kwargs)
    ```

### `#!py class CardDeleteView`

Parents: `DeleteView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class CardDeleteView(DeleteView):
        model: type = PaymentCard
        template_name: str = 'secret/delete_view.html'
        success_url = '/secrets/payment-cards'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Deletion'
            context['model'] = 'Payment Card'
            return context
    ```

### `#!py class NoteCreateView`

Parents: `CreateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class NoteCreateView(CreateView):
        model: type = SecurityNote
        template_name: str = 'secret/create_view.html'
        fields = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Adition'
            context['model'] = 'Security Note'
            return context

        def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
            if not len(r.POST):
                error(r, EMPTY_POST_MSG)
                return HttpResponseRedirect(reverse('secret:note_create_view'))
            if SecurityNote.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
                error(r, FEEDBACK_MSG)
                return super().get(r)
            return super().post(r, *args, **kwargs)
    ```

### `#!py class NoteUpdateView`

Parents: `UpdateView`

Decorators: `#!py login_dec_dispatch`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class NoteUpdateView(UpdateView):
        model: type = SecurityNote
        template_name: str = 'secret/create_view.html'
        fields = '__all__'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Edition'
            context['model'] = 'Security Note'
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

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec_dispatch
    class NoteDeleteView(DeleteView):
        model: type = SecurityNote
        template_name: str = 'secret/delete_view.html'
        success_url = '/secrets/notes'

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context: dict[str, Any] = super().get_context_data(**kwargs)
            context['action'] = 'Deletion'
            context['model'] = 'Security Note'
            return context
    ```



---

## Functions

### `#!py def _list_view`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, secret: Literal['credential', 'card', 'note']`

Kwargs: `#!py None`

Return Type: `#!py dict[str, str | list] | None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def _list_view(r: HttpRequest, secret: Literal['credential', 'card', 'note']) -> dict[str, str | list] | None:
        dispatch: dict[Literal['credential', 'card', 'note'], dict[str, list | str]] = {'credential': {'object_list': r.user.credentials.all(), 'model_name': 'Login Credentials'}, 'card': {'object_list': r.user.cards.all(), 'model_name': 'Payment Cards'}, 'note': {'object_list': r.user.notes.all(), 'model_name': 'Security Notes'}}
        return dispatch.get(secret)
    ```

### `#!py def index`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponseRedirect | HttpResponsePermanentRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def index(r: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        return redirect(reverse('home:index'))
    ```

### `#!py def credential_list_view`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def credential_list_view(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/list_view.html', _list_view(r, 'credential'))
    ```

### `#!py def credential_detail_view`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest, slug: str`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def credential_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
        credential: LoginCredential = get_object_or_404(LoginCredential, owner=r.user, slug=slug)
        return render(r, 'secret/Credential/detail_view.html', {'object': credential})
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adition'
        context['model'] = 'Login Credential'
        return context
    ```

### `#!py def post`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:credential_create_view'))
        if LoginCredential.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edition'
        context['model'] = 'Login Credential'
        return context
    ```

### `#!py def post`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

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

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Deletion'
        context['model'] = 'Login Credential'
        return context
    ```

### `#!py def card_list_view`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def card_list_view(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/list_view.html', _list_view(r, 'card'))
    ```

### `#!py def card_detail_view`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest, slug: str`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def card_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
        card: PaymentCard = get_object_or_404(PaymentCard, owner=r.user, slug=slug)
        return render(r, 'secret/Card/detail_view.html', {'object': card})
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adition'
        context['model'] = 'Payment Card'
        return context
    ```

### `#!py def post`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:card_create_view'))
        if PaymentCard.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edition'
        context['model'] = 'Payment Card'
        return context
    ```

### `#!py def post`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_pk: str | None = r.POST.get('pk')
        filter: dict = dict(owner=r.user, slug=r.POST.get('slug'))
        if PaymentCard.objects.filter(**filter).exclude(pk=post_pk).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Deletion'
        context['model'] = 'Payment Card'
        return context
    ```

### `#!py def note_list_view`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def note_list_view(r: HttpRequest) -> HttpResponse:
        return render(r, 'secret/list_view.html', _list_view(r, 'note'))
    ```

### `#!py def note_detail_view`

Type: `#!py function`

Decorators: `#!py login_dec`

Args: `#!py r: HttpRequest, slug: str`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_dec
    def note_detail_view(r: HttpRequest, slug: str) -> HttpResponse:
        note: SecurityNote = get_object_or_404(SecurityNote, owner=r.user, slug=slug)
        return render(r, 'secret/Note/detail_view.html', {'object': note})
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Adition'
        context['model'] = 'Security Note'
        return context
    ```

### `#!py def post`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def post(self, r: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | HttpResponseRedirect:
        if not len(r.POST):
            error(r, EMPTY_POST_MSG)
            return HttpResponseRedirect(reverse('secret:note_create_view'))
        if SecurityNote.objects.filter(owner=r.user, slug=r.POST.get('slug')).exists():
            error(r, FEEDBACK_MSG)
            return super().get(r)
        return super().post(r, *args, **kwargs)
    ```

### `#!py def get_context_data`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Edition'
        context['model'] = 'Security Note'
        return context
    ```

### `#!py def post`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

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

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py dict[str, Any]`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context['action'] = 'Deletion'
        context['model'] = 'Security Note'
        return context
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
