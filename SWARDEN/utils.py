from io import StringIO
from itertools import compress, product
from typing import Final, Any, Generator, Literal
from hashlib import sha256

from django.core.validators import validate_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.conf import settings

from account.models import User, ActivationAccountToken


SK: str = settings.SECRET_KEY
NO_DATA_TO_EXPORT: Final = "Não há dados para exportação."
SUCCESS_DATA_EXPORTING: Final = "Dados exportados com sucesso."

ACTIVATE_ACCOUNT_TOKEN_SEND: Final = """Sua conta foi criada com sucesso, contudo, você deve ativá-la. Para fazer isso, clique no link abaixo:\n\n\n{domain}/conta/ativar/{uidb64}/{token}\n\n\nEquipe sWarden"""

ACTIVATE_ACCOUNT_CONFIRM_DONE: Final = """A partir de agora a sua conta está ativa e você pode utilizar dos recursos do sistema para armazenar seus dados sensíveis.\n\n\nEquipe sWarden"""


def get_ip_address(r: HttpRequest) -> Any | None:
    x_forwarded_for: Any | None = r.META.get("HTTP_X_FORWARDED_FOR")
    ip: Any | None = (
        x_forwarded_for.split(",")[0] if x_forwarded_for else r.META.get("REMOTE_ADDR")
    )

    return ip


def xor(text: str, key: str, encrypt: bool = True) -> str:
    if text is None or not isinstance(text, str) or not len(key):
        return text

    # Calculate the necessary key repetitions
    key_repetitions: int = max(1, (len(text) + len(key) - 1) // len(key))

    # Expand the key and secret key to match the text length
    expanded_key: str = (key * key_repetitions)[: len(text)]
    expanded_secret_key: str = (SK * key_repetitions)[: len(text)]

    # Create a generator for XORed values
    xor_key_generator: Generator = (
        ord(expanded_key_char) ^ ord(secret_key_char)
        for expanded_key_char, secret_key_char in zip(expanded_key, expanded_secret_key)
    )

    # Encrypt or decrypt the text
    if encrypt:
        transformed_chars = [
            chr((ord(text_char) ^ xor_key_val) + 32)
            for text_char, xor_key_val in zip(text, xor_key_generator)
        ]
    else:
        transformed_chars = [
            chr((ord(text_char) - 32) ^ xor_key_val)
            for text_char, xor_key_val in zip(text, xor_key_generator)
        ]

    return "".join(transformed_chars)


def send_email_activation_account_token(
    domain: str, new_user: User, password: str
) -> None:
    if (
        not isinstance(domain, str)
        or not isinstance(new_user, User)
        or not isinstance(password, str)
    ):
        raise TypeError(f"{domain}, {new_user} and {password} are invalid arguments")

    validate_email(new_user.email)

    token_hash: str = sha256(f"{new_user.username}{password}".encode()).hexdigest()
    uidb64: str = urlsafe_base64_encode(force_bytes(new_user.pk))

    token: ActivationAccountToken = ActivationAccountToken.objects.create(
        value=token_hash,
        user=new_user,
        used=False,
    )

    token.full_clean()

    email: EmailMessage = EmailMessage(
        subject="Ativação de Conta | sWarden",
        body=ACTIVATE_ACCOUNT_TOKEN_SEND.format(
            domain=domain, uidb64=uidb64, token=token_hash
        ),
        from_email=settings.EMAIL_HOST_USER,
        to=[str(new_user.email)],
    )
    email.send()


def send_email_activate_account_completed(user_email: str) -> None:
    validate_email(user_email)

    email: EmailMessage = EmailMessage(
        subject="Ativação de Conta | sWarden",
        body=ACTIVATE_ACCOUNT_CONFIRM_DONE,
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.send()


def send_email_exporting_secrets(
    secret_type: Literal["Credenciais", "Cartões", "Anotações"],
    csvfile: StringIO,
    user_email: str,
) -> None:
    validate_email(user_email)

    email: EmailMessage = EmailMessage(
        subject="Exportação de Segredos | sWarden",
        body=f'Aqui estão seus segredos armazenados em "{secret_type}" no sWarden.\n\n\nEquipe sWarden',
        from_email=settings.EMAIL_HOST_USER,
        to=[user_email],
    )
    email.attach("anotacoes.csv", csvfile.getvalue(), "text/csv")
    email.send()


def create_scenarios(params: list[dict[str, Any]]) -> Generator:
    for case in product([0, 1], repeat=len(params)):
        if all(case):
            break
        temp = compress(params, case)
        temp = list(temp)
        scenario = {}

        for param in temp:
            scenario.update(param)

        yield case, scenario
