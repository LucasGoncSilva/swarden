
# File: `views.py`
Path: `SWARDEN.account`



---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import cast`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import cast
    ```

### `#!py import CaptchaField`

Path: `#!py captcha.fields`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from captcha.fields import CaptchaField
    ```

### `#!py import authenticate`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import authenticate
    ```

### `#!py import login`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import login
    ```

### `#!py import logout`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import logout
    ```

### `#!py import login_required`

Path: `#!py django.contrib.auth.decorators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.decorators import login_required
    ```

### `#!py import AbstractBaseUser`

Path: `#!py django.contrib.auth.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth.models import AbstractBaseUser
    ```

### `#!py import error`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import error
    ```

### `#!py import success`

Path: `#!py django.contrib.messages`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.messages import success
    ```

### `#!py import CharField`

Path: `#!py django.forms`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.forms import CharField
    ```

### `#!py import EmailField`

Path: `#!py django.forms`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.forms import EmailField
    ```

### `#!py import Form`

Path: `#!py django.forms`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.forms import Form
    ```

### `#!py import PasswordInput`

Path: `#!py django.forms`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.forms import PasswordInput
    ```

### `#!py import TextInput`

Path: `#!py django.forms`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.forms import TextInput
    ```

### `#!py import Http404`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import Http404
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

### `#!py import force_str`

Path: `#!py django.utils.encoding`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.encoding import force_str
    ```

### `#!py import urlsafe_base64_decode`

Path: `#!py django.utils.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.utils.http import urlsafe_base64_decode
    ```

### `#!py import send_email_activate_account_completed`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import send_email_activate_account_completed
    ```

### `#!py import send_email_activation_account_token`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import send_email_activation_account_token
    ```

### `#!py import ActivationAccountToken`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import ActivationAccountToken
    ```

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class RegisterForm`

Parents: `Form`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class RegisterForm(Form):
        username: Final[CharField] = CharField(label='', max_length=50, required=True, widget=TextInput(attrs={'placeholder': 'Username (nome de usuário)*', 'class': 'py-2', 'style': 'text-align: center;', 'autofocus': 'autofocus'}), help_text='50 caracteres ou menos. Letras, números e @/./+/-/_ apenas.')
        first_name: Final[CharField] = CharField(label='', required=True, widget=TextInput(attrs={'placeholder': 'Nome*', 'class': 'mt-3 py-2', 'style': 'text-align: center;'}))
        last_name: Final[CharField] = CharField(label='', required=True, widget=TextInput(attrs={'placeholder': 'Sobrenome*', 'class': 'py-2', 'style': 'text-align: center;'}))
        email: Final[EmailField] = EmailField(label='', required=True, widget=TextInput(attrs={'placeholder': 'Email*', 'class': 'mt-3 py-2', 'style': 'text-align: center;'}))
        password: Final[CharField] = CharField(label='', required=True, widget=PasswordInput(attrs={'placeholder': 'Senha*', 'class': 'mt-3 py-2', 'style': 'text-align: center;'}))
        password2: Final[CharField] = CharField(label='', required=True, widget=PasswordInput(attrs={'placeholder': 'Confirmação de senha*', 'class': 'mb-5 py-2', 'style': 'text-align: center;'}))
        captcha: Final[CaptchaField] = CaptchaField()
    ```

### `#!py class LogInForm`

Parents: `Form`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class LogInForm(Form):
        username: Final[CharField] = CharField(label='', required=True, widget=TextInput(attrs={'placeholder': 'Username*', 'class': 'py-2', 'style': 'text-align: center;', 'autofocus': 'autofocus'}))
        password: Final[CharField] = CharField(label='', required=True, widget=PasswordInput(attrs={'placeholder': 'Pass*', 'class': 'mt-3 py-2', 'style': 'text-align: center;'}))
    ```



---

## Functions

### `#!py def register_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def register_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        elif r.method != 'POST':
            form: Form = RegisterForm()
            return render(r, 'account/register.html', {'form': form})
        form: Form = RegisterForm(r.POST)
        if not form.is_valid():
            return render(r, 'account/register.html', {'form': form})
        password: str | None = form.cleaned_data.get('password')
        password2: str | None = form.cleaned_data.get('password2')
        if not password or not password2 or password != password2:
            error(r, 'Senhas não compatíveis')
            return render(r, 'account/register.html', {'form': form})
        username: str | None = form.cleaned_data.get('username')
        email: str | None = form.cleaned_data.get('email')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or username is None or (email is None):
            error(r, 'Username e/ou e-mail indisponível')
            return render(r, 'account/register.html', {'form': form})
        first_name: str = cast(str, form.cleaned_data.get('first_name'))
        last_name: str = cast(str, form.cleaned_data.get('last_name'))
        user: User = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_active=False)
        send_email_activation_account_token(r.get_host(), user, password)
        success(r, 'Conta criada. Acesse seu e-mail para ativar sua conta.')
        return HttpResponseRedirect(reverse('account:login'))
    ```

### `#!py def activate_account_missing_parameter`

Type: `#!py ...`

Return Type: `#!py HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, uidb64: str | None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def activate_account_missing_parameter(r: HttpRequest, uidb64: str | None=None) -> HttpResponseRedirect:
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def activate_account`

Type: `#!py ...`

Return Type: `#!py HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py r: HttpRequest, uidb64: str, token: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def activate_account(r: HttpRequest, uidb64: str, token: str) -> HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        user: User | None = None
        try:
            id: int = int(force_str(urlsafe_base64_decode(uidb64)))
            user = get_object_or_404(User, pk=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Http404()
        token_obj: ActivationAccountToken = get_object_or_404(ActivationAccountToken, value=token, used=False)
        user.is_active = True
        user.save()
        token_obj.used = True
        token_obj.save()
        login(r, user)
        send_email_activate_account_completed(str(user.email))
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def login_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def login_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:index'))
        elif r.method != 'POST':
            return render(r, 'account/login.html', {'form': LogInForm()})
        form: Final[Form] = LogInForm(r.POST)
        if not form.is_valid():
            return render(r, 'account/login.html', {'form': form})
        username: Final[str] = str(form.cleaned_data.get('username')).strip()
        password: Final[str] = str(form.cleaned_data.get('password')).strip()
        user: AbstractBaseUser | None = authenticate(username=username, password=password)
        if user is None:
            error(r, 'Username e/ou senha inválida')
            return render(r, 'account/login.html', {'form': form})
        login(r, user)
        return HttpResponseRedirect(reverse('home:index'))
    ```

### `#!py def logout_view`

Type: `#!py ...`

Return Type: `#!py HttpResponse | HttpResponseRedirect`

Decorators: `#!py login_required(login_url='/conta/entrar')`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @login_required(login_url='/conta/entrar')
    def logout_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
        if r.method == 'POST':
            logout(r)
            return HttpResponseRedirect(reverse('account:login'))
        return render(r, 'account/logout.html')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
