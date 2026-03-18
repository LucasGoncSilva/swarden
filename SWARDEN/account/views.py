from random import sample
from typing import Final, cast

from CORE.utils import bind_log_data
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.messages import error, success
from django.forms import CharField
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables

from account.forms import (
    LogInForm,
    RecoveryTestForm,
    RecoveryWordlistForm,
    RegisterForm,
)
from account.models import (
    ActivationAccountToken,
    RecoveryPhrase,
    User,
)


@sensitive_post_parameters()
@sensitive_variables()
def register(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return redirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/register.html', {'form': RegisterForm()})

    form: RegisterForm = RegisterForm(r.POST)

    if not form.is_valid():
        error(r, 'Please fill the form correctly.')
        return render(r, 'account/register.html', {'form': form}, status=422)

    form.full_clean()

    passphrase: CharField = form.data['passphrase']
    passphrase2: CharField = form.data['passphrase2']

    if passphrase != passphrase2:
        error(r, 'Passphrases does not match.')
        return render(r, 'account/register.html', {'form': form}, status=422)

    username: CharField = form.data['username']

    if User.objects.filter(username=username).count() > 0:
        error(r, 'Invalid or unavailable username.')
        return render(r, 'account/register.html', {'form': form}, status=422)

    user: User = User.objects.create_user(
        username=str(username),
        password=str(passphrase2),
        is_active=False,
    )

    activate_token: ActivationAccountToken = (
        ActivationAccountToken.create_activation_account_token(user)
    )
    uidb64_token: str = user.pk_uidb64

    success(r, 'Account created. Activate it below.')
    return redirect(reverse('account:activate', args=(uidb64_token, activate_token)))


def activate_account_missing_parameter(
    r: HttpRequest, uidb64: str | None = None
) -> HttpResponseRedirect:
    bind_log_data(uidb64=uidb64)
    return redirect(reverse('home:index'))


@sensitive_post_parameters()
@sensitive_variables()
def activate_account(
    r: HttpRequest, uidb64: str, token: str
) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return redirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/activate_account.html', {'form': LogInForm()})

    form: Final[LogInForm] = LogInForm(r.POST)

    if not form.is_valid():
        error(r, 'Please fill the form correctly.')
        return render(r, 'account/activate_account.html', {'form': form}, status=422)

    try:
        uuid: str = force_str(urlsafe_base64_decode(uidb64))
        user: User = get_object_or_404(User, pk=uuid, is_active=False)

    except TypeError, ValueError, OverflowError, User.DoesNotExist:
        raise Http404()

    token_obj: ActivationAccountToken = get_object_or_404(
        ActivationAccountToken, value=token, used=False
    )

    form.full_clean()

    username: CharField = form.data['username']
    passphrase: CharField = form.data['passphrase']

    user.is_active = True  # type: ignore
    user.save()

    if not authenticate(username=str(username), password=str(passphrase)) == user:
        user.is_active = False  # type: ignore
        user.save()

        error(r, 'Invalid username and/or passphrase')
        return render(r, 'account/activate_account.html', {'form': form}, status=422)

    token_obj.used = True
    token_obj.save()
    auth_login(r, user)

    success(r, 'Account activated successfully!')
    return redirect(reverse('account:wordlist'))


@sensitive_post_parameters()
@sensitive_variables()
@login_required
def wordlist(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if RecoveryPhrase.objects.filter(user=r.user, is_active=True).count() > 0:
        return redirect(reverse('home:index'))

    elif r.method == 'POST':
        form: RecoveryTestForm = RecoveryTestForm(r.POST)

        if not form.is_valid():
            error(r, 'Please fill the form correctly.')
            bind_log_data(form=form)
            return redirect(reverse('account:wordlist'))

        form.full_clean()

        word1: str | None = form.data['word1']
        word2: str | None = form.data['word2']
        word3: str | None = form.data['word3']

        test_order_comp: list[str] = list(
            cast(dict[int, str], r.session.get('test_order')).values()
        )

        if [word1, word2, word3] != test_order_comp:
            error(r, 'You missed. Pay attention now.')
            bind_log_data(
                form=form,
                word1=word1,
                word2=word2,
                word3=word3,
                test_order=test_order_comp,
            )
            return redirect(reverse('account:wordlist'))

        RecoveryPhrase.objects.filter(user=r.user, is_active=False).update(
            is_active=True
        )
        del r.session['test_order']
        success(r, '12-words recovery list completed successfully. Do not lose it.')
        return redirect(reverse('home:index'))

    words: list[str] = RecoveryPhrase.create_user_recovery(r.user).split()

    test_order: dict[int, str] = {}
    test_words: list[str] = sample(words, k=3)

    for i in test_words:
        test_order[words.index(i) + 1] = i

    r.session['test_order'] = test_order

    return render(
        r,
        'account/wordlist.html',
        {
            'form': RecoveryTestForm(),
            'wordlist': {i: word for i, word in enumerate(words, start=1)},
            'test_order': test_order,
        },
    )


@sensitive_post_parameters()
@sensitive_variables()
def login(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return redirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/login.html', {'form': LogInForm()})

    form: Final[LogInForm] = LogInForm(r.POST)

    if not form.is_valid():
        error(r, 'Please fill the form correctly.')
        bind_log_data(form=form)
        return render(r, 'account/login.html', {'form': form}, status=422)

    form.full_clean()

    username: Final[str] = str(form.data['username'])
    passphrase: Final[str] = str(form.data['passphrase'])

    user: AbstractBaseUser | None = authenticate(username=username, password=passphrase)

    if user is None:
        error(r, 'Invalid username and/or passphrase')
        return render(r, 'account/login.html', {'form': form}, status=422)

    auth_login(r, user)
    return redirect(reverse('home:index'))


@sensitive_post_parameters()
@sensitive_variables()
def recovery(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.user.is_authenticated:
        return redirect(reverse('home:index'))

    elif r.method != 'POST':
        return render(r, 'account/recovery.html', {'form': RecoveryWordlistForm()})

    form: RecoveryWordlistForm = RecoveryWordlistForm(r.POST)

    if not form.is_valid():
        error(r, 'Please fill the form correctly.')
        bind_log_data(form=form)
        return render(r, 'account/recovery.html', {'form': form}, status=422)

    words: list[str] = []
    form.full_clean()

    for i in range(12):
        words.append(form.data[f'word{i + 1}'])

    phrase: str = ' '.join(words).lower()
    fingerprint: str = RecoveryPhrase.generate_fingerprint(phrase)

    try:
        recovery: RecoveryPhrase = RecoveryPhrase.objects.select_related('user').get(
            fingerprint=fingerprint
        )

        if not recovery.is_valid_phrase(phrase):
            raise RecoveryPhrase.DoesNotExist('RecoveryPhrase hash does not match.')

    except RecoveryPhrase.DoesNotExist:
        error(r, 'Something went wrong with provided words. Please review them.')
        bind_log_data(form=form, fingerprint=fingerprint)
        return render(r, 'account/recovery.html', {'form': form}, status=422)

    user: User = recovery.user

    auth_login(r, user)
    success(r, 'Success on recovery list login!')
    return redirect(reverse('home:index'))


@sensitive_post_parameters()
@sensitive_variables()
@login_required
def logout(r: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if r.method == 'POST':
        auth_logout(r)
        return redirect(reverse('account:login'))

    return render(r, 'account/logout.html')
