from typing import Final

from captcha.fields import CaptchaField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.messages import error, success
from django.forms import CharField, Form, PasswordInput, TextInput
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from account.models import ActivationAccountToken, User


class RegisterForm(Form):
    username: Final[CharField] = CharField(
        label='Username',
        min_length=2,
        max_length=20,
        required=True,
        widget=TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Enter your username',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
            }
        ),
        help_text='Max of 20 chars. Letters, numbers and "@", ".", "+", "-", "_" only.',
    )
    passphrase: Final[CharField] = CharField(
        label='Passphrase',
        required=True,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase',
                'placeholder': 'Enter your passphrase',
                'autocomplete': 'off',
            }
        ),
        help_text='Use a "passphase", sentence '
        'instead of random characters or just password.',
    )
    passphrase2: Final[CharField] = CharField(
        label='',
        required=True,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase-confirm',
                'placeholder': 'Confirm your passphrase',
                'autocomplete': 'off',
            }
        ),
    )
    captcha: Final[CaptchaField] = CaptchaField()


class LogInForm(Form):
    username: Final[CharField] = CharField(
        label='Username',
        min_length=2,
        max_length=32,
        required=True,
        widget=TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Enter your username',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
            }
        ),
    )
    passphrase: Final[CharField] = CharField(
        label='Passphrase',
        required=True,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase',
                'placeholder': 'Enter your passphrase',
                'autocomplete': 'off',
            }
        ),
    )


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
    print(username, passphrase)

    User.objects.create_user(  # type: ignore
        username=username,
        password=passphrase,
        is_active=False,
    )

    success(r, 'Conta criada. Acesse seu e-mail para ativar sua conta.')
    return HttpResponseRedirect(reverse('account:login'))


def activate_account_missing_parameter(
    r: HttpRequest, uidb64: str | None = None
) -> HttpResponseRedirect:
    return HttpResponseRedirect(reverse('home:index'))


def activate_account(r: HttpRequest, uidb64: str, token: str) -> HttpResponseRedirect:
    if r.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))

    user: User | None = None

    try:
        id: int = int(force_str(urlsafe_base64_decode(uidb64)))
        user = get_object_or_404(User, pk=id)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        raise Http404()

    token_obj: ActivationAccountToken = get_object_or_404(
        ActivationAccountToken, value=token, used=False
    )

    user.is_active = True
    user.save()

    token_obj.used = True
    token_obj.save()

    login(r, user)

    return HttpResponseRedirect(reverse('home:index'))


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
    print(username, passphrase)

    user: AbstractBaseUser | None = authenticate(username=username, password=passphrase)
    print(user)

    if user is None:
        error(r, 'Invalid username and/or passphrase')
        return render(r, 'account/login.html', {'form': form})

    login(r, user)
    return HttpResponseRedirect(reverse('home:index'))


@login_required(login_url='/account/login')
def logout_view(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.method == 'POST':
        logout(r)
        return HttpResponseRedirect(reverse('account:login'))

    return render(r, 'account/logout.html')
