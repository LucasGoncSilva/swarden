# File: `views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account`

No file docstring provided.

---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import authenticate`

Path: `#!py django.contrib.auth`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth import authenticate
    ```

### `#!py import login`

Path: `#!py django.contrib.auth`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth import login
    ```

### `#!py import logout`

Path: `#!py django.contrib.auth`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth import logout
    ```

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import AbstractBaseUser`

Path: `#!py django.contrib.auth.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.models import AbstractBaseUser
    ```

### `#!py import error`

Path: `#!py django.contrib.messages`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.messages import error
    ```

### `#!py import success`

Path: `#!py django.contrib.messages`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.messages import success
    ```

### `#!py import Http404`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import Http404
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

### `#!py import force_str`

Path: `#!py django.utils.encoding`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.encoding import force_str
    ```

### `#!py import urlsafe_base64_decode`

Path: `#!py django.utils.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.http import urlsafe_base64_decode
    ```

### `#!py import create_activation_account_token`

Path: `#!py utils`

Category: trdparty

??? example "Snippet"

    ```py
    from utils import create_activation_account_token
    ```

### `#!py import uidb64`

Path: `#!py utils`

Category: trdparty

??? example "Snippet"

    ```py
    from utils import uidb64
    ```

### `#!py import LogInForm`

Path: `#!py account.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from account.forms import LogInForm
    ```

### `#!py import RegisterForm`

Path: `#!py account.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from account.forms import RegisterForm
    ```

### `#!py import ActivationAccountToken`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import ActivationAccountToken
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def register_view`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def register_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        elif r.method != 'POST':
            form: RegisterForm = RegisterForm()
            return render(r, 'account/register.html', {'form': form})
        form: RegisterForm = RegisterForm(r.POST)
        if not form.is_valid():
            return render(r, 'account/register.html', {'form': form})
        passphrase: str | None = form.cleaned_data.get('passphrase')
        passphrase2: str | None = form.cleaned_data.get('passphrase2')
        if not passphrase or not passphrase2 or passphrase != passphrase2:
            error(r, 'Passphrases does not match.')
            return render(r, 'account/register.html', {'form': form})
        username: str | None = form.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() or username is None:
            error(r, 'Username unavailable')
            return render(r, 'account/register.html', {'form': form})
        user: User = User.objects.create_user(username=username, password=passphrase, is_active=False)
        activate_token: ActivationAccountToken = create_activation_account_token(user)
        uidb64_token: str = uidb64(user.pk)
        success(r, 'Account created. Activate it below.')
        return HttpResponseRedirect(reverse('account:activate', args=(uidb64_token, activate_token)))
    ```

### `#!py def activate_account_missing_parameter`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, uidb64: str | None`

Kwargs: `#!py None`

Return Type: `#!py HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def activate_account_missing_parameter(r: HttpRequest, uidb64: str | None=None) -> HttpResponseRedirect:
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def activate_account`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, uidb64: str, token: str`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def activate_account(r: HttpRequest, uidb64: str, token: str) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        elif r.method != 'POST':
            return render(r, 'account/activate_account.html', {'form': LogInForm()})
        form: Final[LogInForm] = LogInForm(r.POST)
        if not form.is_valid():
            return render(r, 'account/activate_account.html', {'form': form})
        user: User | None = None
        try:
            uuid: str = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uuid, is_active=False)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Http404()
        token_obj: ActivationAccountToken = get_object_or_404(ActivationAccountToken, value=token, used=False)
        username: Final[str] = str(form.cleaned_data.get('username'))
        passphrase: Final[str] = str(form.cleaned_data.get('passphrase'))
        user.is_active = True
        user.save()
        if not authenticate(username=username, password=passphrase) == user:
            user.is_active = False
            user.save()
            error(r, 'Invalid username and/or passphrase')
            return render(r, 'account/activate_account.html', {'form': form})
        token_obj.used = True
        token_obj.save()
        login(r, user)
        success(r, 'Account activated successfully!')
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def login_view`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def login_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        elif r.method != 'POST':
            return render(r, 'account/login.html', {'form': LogInForm()})
        form: Final[LogInForm] = LogInForm(r.POST)
        if not form.is_valid():
            return render(r, 'account/login.html', {'form': form})
        username: Final[str] = str(form.cleaned_data.get('username'))
        passphrase: Final[str] = str(form.cleaned_data.get('passphrase'))
        user: AbstractBaseUser | None = authenticate(username=username, password=passphrase)
        if user is None:
            error(r, 'Invalid username and/or passphrase')
            return render(r, 'account/login.html', {'form': form})
        login(r, user)
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def logout_view`

Type: `#!py function`

Decorators: `#!py login_required(login_url='/account/login')`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @login_required(login_url='/account/login')
    def logout_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.method == 'POST':
            logout(r)
            return HttpResponseRedirect(reverse('account:login'))
        return render(r, 'account/logout.html')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
