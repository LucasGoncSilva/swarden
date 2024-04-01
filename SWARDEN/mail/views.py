from typing import Final, Literal, Type
from csv import writer
from hashlib import sha256
from io import StringIO

from django.db import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseServerError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.messages import success, error

from account.models import User, ActivationAccountToken
from secret.models import Card, LoginCredential, SecurityNote


# Create your views here.
NO_DATA_TO_EXPORT: Final = 'Não há dados para exportação.'
SUCCESS_DATA_EXPORTING: Final = 'Dados exportados com sucesso.'

ACTIVATE_ACCOUNT_TOKEN_SEND: Final = (
    """Sua conta foi criada com sucesso, contudo, você deve ativá-la. Para fazer isso, clique no link abaixo:\n\n\n{domain}/conta/ativar/{uidb64}/{token}\n\n\nEquipe sWarden"""
)

ACTIVATE_ACCOUNT_CONFIRM_DONE: Final = (
    """A partir de agora a sua conta está ativa e você pode utilizar dos recursos do sistema para armazenar seus dados sensíveis.\n\n\nEquipe sWarden"""
)


def export_secrets(
    r: HttpRequest, secret_type: Literal['Credenciais', 'Cartões', 'Anotações']
) -> HttpResponseRedirect:
    CREDENTIALS: Final[str] = 'Credenciais'
    CARDS: Final[str] = 'Cartões'
    SECURITY_NOTES: Final[str] = 'Anotações'

    if secret_type not in [CREDENTIALS, CARDS, SECURITY_NOTES]:
        return HttpResponseRedirect(reverse('home:index'))

    dispatch_models: dict[
        str, Type[LoginCredential] | Type[Card] | Type[SecurityNote]
    ] = {CREDENTIALS: LoginCredential, CARDS: Card, SECURITY_NOTES: SecurityNote}

    query: QuerySet = dispatch_models[secret_type].objects.filter(owner=r.user)

    if not query.exists():
        error(r, NO_DATA_TO_EXPORT)

        dispatch_redirect: dict[str, str] = {
            CREDENTIALS: 'secret:credential_list_view',
            CARDS: 'secret:card_list_view',
            SECURITY_NOTES: 'secret:note_list_view',
        }
        return HttpResponseRedirect(reverse(dispatch_redirect[secret_type]))

    csvfile: StringIO = StringIO()
    csvwriter = writer(csvfile, delimiter='¬', doublequote=True)

    email: EmailMessage = EmailMessage(
        subject='Exportação de Segredos | sWarden',
        body=f'Aqui estão seus segredos armazenados em "{secret_type}" no sWarden.\n\n\nEquipe sWarden',
        from_email=settings.EMAIL_HOST_USER,
        to=[r.user.email],
    )

    if secret_type == CREDENTIALS:
        csvwriter.writerow(
            ['Serviço', 'Apelido', 'Login 3rd', 'Apelido Login 3rd', 'Login', 'Senha']
        )

        for i in query:
            csvwriter.writerow(
                [
                    i.get_service_display(),
                    i.name,
                    i.thirdy_party_login,
                    i.thirdy_party_login_name,
                    i.login,
                    i.password,
                ]
            )

        email.attach('credenciais.csv', csvfile.getvalue(), 'text/csv')
        email.send()

        success(r, SUCCESS_DATA_EXPORTING)
        return HttpResponseRedirect(reverse('secret:credential_list_view'))

    elif secret_type == CARDS:
        csvwriter.writerow(
            [
                'Apelido',
                'Tipo',
                'Número',
                'Expiração',
                'CVV',
                'Banco',
                'Bandeira',
                'Titular',
            ]
        )

        for i in query:
            csvwriter.writerow(
                [
                    i.name,
                    i.get_card_type_display(),
                    i.number,
                    i.expiration,
                    i.cvv,
                    i.get_bank_display(),
                    i.get_brand_display(),
                    i.owners_name,
                ]
            )

        email.attach('cartoes.csv', csvfile.getvalue(), 'text/csv')
        email.send()

        success(r, SUCCESS_DATA_EXPORTING)
        return HttpResponseRedirect(reverse('secret:card_list_view'))

    elif secret_type == SECURITY_NOTES:
        csvwriter.writerow(['Título', 'Conteúdo'])

        for i in query:
            csvwriter.writerow([i.title, i.content])

        email.attach('anotacoes.csv', csvfile.getvalue(), 'text/csv')
        email.send()

        success(r, SUCCESS_DATA_EXPORTING)
        return HttpResponseRedirect(reverse('secret:note_list_view'))


def send_activate_account_token(domain: str, user: User, password: str) -> None:
    token_hash = sha256(f'{user.username}{password}'.encode()).hexdigest()
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    token: ActivationAccountToken = ActivationAccountToken.objects.create(
        value=token_hash, used=False
    )

    try:
        print('validating token')
        token.full_clean()
        if not token.is_valid():
            token.failed = True
            raise ValidationError(
                f'ActivationAccountToken(value={token.value}, used={token.used}, created={token.created}) is invalid.'
            )
    except (DataError, IntegrityError, ValidationError) as e:
        raise e

    email: EmailMessage = EmailMessage(
        subject='Ativação de Conta | sWarden',
        body=ACTIVATE_ACCOUNT_TOKEN_SEND.format(
            domain=domain, uidb64=uidb64, token=token_hash
        ),
        from_email=settings.EMAIL_HOST_USER,
        to=[str(user.email)],
    )
    email.send()


def send_activate_account_done(user_email: str) -> None:
    email: EmailMessage = EmailMessage(
        subject='Ativação de Conta | sWarden',
        body=ACTIVATE_ACCOUNT_CONFIRM_DONE,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.send()
