from typing import Final, Literal
from csv import writer
from hashlib import sha256
from io import StringIO

from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpRequest, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages

from account.models import User, ActivationAccountToken
from secret.models import Card, LoginCredential, SecurityNote


# Create your views here.
ACTIVATE_ACCOUNT_TOKEN_SEND: Final = """
Sua conta foi criada com sucesso, contudo, você deve ativá-la. Para fazer isso, clique no link abaixo:

{domain}/conta/ativar/{uidb64}/{token}


Equipe sWarden
"""

ACTIVATE_ACCOUNT_CONFIRM_DONE: Final = """
A partir de agora a sua conta está ativa e você pode utilizar dos recursos do sistema para armazenar seus dados sensíveis.


Equipe sWarden
"""


def export_secrets(
    r: HttpRequest, secret_type: Literal['Credenciais', 'Cartões', 'Anotações']
) -> HttpResponseRedirect:
    csvfile: StringIO = StringIO()
    csvwriter = writer(csvfile, delimiter='¬', doublequote=True)

    email: EmailMessage = EmailMessage(
        subject='Exportação de Segredos | sWarden',
        body=f'Aqui estão seus segredos armazenados em "{secret_type}" no sWarden.\n\n\nEquipe sWarden',
        from_email=settings.EMAIL_HOST_USER,
        to=[r.user.email],
    )

    if secret_type == 'Credenciais':
        if not LoginCredential.objects.filter(owner=r.user).exists():
            messages.error(r, 'Não há credenciais para exportar.')
            return HttpResponseRedirect(reverse('secret:credential_list_view'))

        csvwriter.writerow(
            ['Serviço', 'Apelido', 'Login 3rd', 'Apelido Login 3rd', 'Login', 'Senha']
        )

        for i in LoginCredential.objects.filter(owner=r.user):
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

        messages.success(r, 'Credenciais exportadas com sucesso.')
        return HttpResponseRedirect(reverse('secret:credential_list_view'))

    elif secret_type == 'Cartões':
        if not Card.objects.filter(owner=r.user).exists():
            messages.error(r, 'Não há cartões para exportar.')
            return HttpResponseRedirect(reverse('secret:card_list_view'))

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

        for i in Card.objects.filter(owner=r.user):
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

        messages.success(r, 'Cartões exportados com sucesso.')
        return HttpResponseRedirect(reverse('secret:card_list_view'))

    elif secret_type == 'Anotações':
        if not SecurityNote.objects.filter(owner=r.user).exists():
            messages.error(r, 'Não há anotações para exportar.')
            return HttpResponseRedirect(reverse('secret:note_list_view'))

        csvwriter.writerow(['Título', 'Conteúdo'])

        for i in SecurityNote.objects.filter(owner=r.user):
            csvwriter.writerow([i.title, i.content])

        email.attach('anotacoes.csv', csvfile.getvalue(), 'text/csv')
        email.send()

        messages.success(r, 'Anotações exportadas com sucesso.')
        return HttpResponseRedirect(reverse('secret:note_list_view'))

    else:
        return HttpResponseRedirect(reverse('home:index'))


def send_activate_account_token(domain: str, user: User, password: str) -> None:
    token_hash = sha256(f'{user.username}{password}'.encode()).hexdigest()
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    ActivationAccountToken.objects.create(value=token_hash, used=False)

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
