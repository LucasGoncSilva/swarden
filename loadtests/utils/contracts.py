from typing import TypedDict


class CredentialContract(TypedDict):
    csrfmiddlewaretoken: str
    pk: str | None
    name: str
    service: str
    slug: str
    third_party_login: bool
    third_party_login_name: str
    login: str
    password: str


class CardContract(TypedDict):
    csrfmiddlewaretoken: str
    pk: str | None
    name: str
    owners_name: str
    card_type: str
    number: str
    expiration_0: int
    expiration_1: int
    cvv: str
    bank: str
    brand: str
    branch: str
    account: str
    password: str
    slug: str


class NoteContract(TypedDict):
    csrfmiddlewaretoken: str
    pk: str | None
    title: str
    content: str
    note_type: str
    slug: str
