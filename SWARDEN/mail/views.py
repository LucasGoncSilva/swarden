from csv import writer
from io import StringIO
from typing import Final, Literal, cast

from account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success, warning
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from secret.models import Card, LoginCredential, SecurityNote
from utils import (
    NO_DATA_TO_EXPORT,
    SUCCESS_DATA_EXPORTING,
    send_email_exporting_secrets,
)

from mail.models import WakeDatabase


@login_required(login_url='/conta/entrar')
def export_secrets_no_argument(r: HttpRequest):
    return HttpResponseRedirect(reverse('home:index'))


@login_required(login_url='/conta/entrar')
def export_secrets(
    r: HttpRequest, secret_type: Literal['Credenciais', 'Cartões', 'Anotações']
) -> HttpResponseRedirect:
    CREDENTIALS: Final[str] = 'Credenciais'
    CARDS: Final[str] = 'Cartões'
    SECURITY_NOTES: Final[str] = 'Anotações'

    if secret_type not in [CREDENTIALS, CARDS, SECURITY_NOTES]:
        warning(r, 'Impossível exportar segredos do tipo informado.')
        return HttpResponseRedirect(reverse('home:index'))

    dispatch_models: dict[
        str, type[LoginCredential] | type[Card] | type[SecurityNote]
    ] = {CREDENTIALS: LoginCredential, CARDS: Card, SECURITY_NOTES: SecurityNote}

    query: QuerySet = dispatch_models[secret_type].objects.filter(owner=r.user)

    dispatch_redirect: dict[str, str] = {
        CREDENTIALS: 'secret:credential_list_view',
        CARDS: 'secret:card_list_view',
        SECURITY_NOTES: 'secret:note_list_view',
    }

    if not query.exists():
        error(r, NO_DATA_TO_EXPORT)
        return HttpResponseRedirect(reverse(dispatch_redirect[secret_type]))

    csvfile: StringIO = StringIO()
    csvwriter = writer(csvfile, delimiter='¬', doublequote=True)

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

    elif secret_type == SECURITY_NOTES:
        csvwriter.writerow(['Título', 'Conteúdo'])

        for i in query:
            csvwriter.writerow([i.title, i.content])

    send_email_exporting_secrets(secret_type, csvfile, cast(User, r.user).email)
    success(r, SUCCESS_DATA_EXPORTING)
    return HttpResponseRedirect(reverse(dispatch_redirect[secret_type]))


def wake_db(r: HttpRequest) -> HttpResponse:
    WakeDatabase.objects.create()

    e = WakeDatabase.objects.all()

    if e.count() > 3:
        e.delete()

    return HttpResponse(e.count())
