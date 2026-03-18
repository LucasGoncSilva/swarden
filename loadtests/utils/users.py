from pathlib import Path
from random import choice, randint
from typing import Final, cast

from bs4 import BeautifulSoup, Tag
from faker import Faker
from locust import HttpUser, between, task
from slugify import slugify

from .contracts import CardContract, CredentialContract, NoteContract


USERS_LIST: list[tuple[str, str]] = []
USERS_PATH: Final[Path] = (
    Path(__file__)
    .resolve()
    .parent.parent.parent.joinpath(
        'SWARDEN/account/management/commands/populateuser.txt'
    )
)

with open(USERS_PATH, encoding='utf-8') as f:
    lines: list[str] = f.readlines()

    for i in lines:
        username, passphrase = i.strip().split('::')
        USERS_LIST.append((username, passphrase))


class DjangoUser(HttpUser):
    """Base-user for Django access and TaskSet fulfillment"""

    abstract: bool = True
    wait_time = between(1, 3)
    F: Faker = Faker()

    def on_start(self) -> None:
        """
        Logs the user in when a new DjangoUser is initiated

        Accessing with GET /account/login and obtaining a session `csrftoken`,
        using that same `csrftoken` with POST /account/login and, in this way,
        obtaining a logged-in virtual user.
        """

        response = self.client.get('/account/login')

        csrftoken: str = response.cookies['crosstoken']

        self.username, self.passphrase = choice(USERS_LIST)

        with self.client.post(
            '/account/login',
            {
                'csrfmiddlewaretoken': csrftoken,
                'username': self.username,
                'passphrase': self.passphrase,
            },
            headers={
                'X-CSRFToken': csrftoken,
                'Referer': f'{self.host}/account/login/',
            },
            name='/account/login',
            catch_response=True,
        ) as response:
            soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

            username_tag = soup.find('span', attrs={'id': 'username'})

            if username_tag is None:
                response.failure('Login failure: username_tag is None')
                self.environment.events.user_error.fire(
                    user_instance=self, exception=Exception('Login Failed'), tb=None
                )
                self.client.close()

            elif username_tag.text == self.username and (
                response.status_code == 200 or response.is_redirect
            ):
                response.success()

            else:
                response.failure(f'Login failure: status code = {response.status_code}')
                self.environment.events.user_error.fire(
                    user_instance=self, exception=Exception('Login Failed'), tb=None
                )
                self.client.close()

    @task
    def get_secrets(self) -> None:
        self.client.get('/secrets', name='/secrets')

    @task
    def get_credentials(self) -> None:
        self.client.get('/secrets/credentials/', name='/secrets/credentials/')

    @task
    def get_payment_cards(self) -> None:
        self.client.get('/secrets/payment-cards/', name='/secrets/payment-cards/')

    @task
    def get_notes(self) -> None:
        self.client.get('/secrets/notes/', name='/secrets/notes/')

    @task
    def credential_crud(self) -> None:
        """Flow for LoginCredential CRUD"""

        # ===== CREATE =====
        with self.client.get(
            '/secrets/credentials/new',
            name='/secrets/credentials/new',
            catch_response=True,
        ) as response:
            try:
                self.csrftoken: str = response.cookies['crosstoken'].strip()

                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

                service_options = cast(
                    Tag, soup.find('select', attrs={'name': 'service'})
                ).find_all('option')
                valid_service_options = [
                    opt for opt in service_options if opt.get('value')
                ]

                chosen_service = choice(valid_service_options)

                service_uuid: str = str(chosen_service.get('value')).strip()
                service_name: str = chosen_service.text.strip()

                name: str = self.F.sentence(nb_words=4)[:10].strip()

                slug: str = slugify(f'{service_name} {name}').strip()

                response.success()

            except AttributeError:
                response.failure(f'Page not correctly loaded: {response.status_code=}')
                return

        with self.client.post(
            '/secrets/credentials/new',
            CredentialContract(
                csrfmiddlewaretoken=self.csrftoken,
                pk=None,
                name=name,
                service=service_uuid,
                slug=slug,
                third_party_login=False,
                third_party_login_name='-----',
                login=self.F.user_name().strip(),
                password=self.F.password().strip(),
            ),
            name='/secrets/credentials/new',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/credentials/new',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and slug in response.headers.get('Location', ''):
                response.success()
            else:
                response.failure(
                    f'Create failure: status code = {response.status_code}'
                )
        # ==================

        # ====== READ ======
        with self.client.get(
            f'/secrets/credentials/{slug}',
            name='/secrets/credentials/<slug>',
            catch_response=True,
        ) as response:
            if service_name in response.text and (
                response.status_code == 200 or response.is_redirect
            ):
                response.success()
            else:
                response.failure(f'Read failure: status code = {response.status_code}')
        # ==================

        # ===== UPDATE =====
        with self.client.get(
            f'/secrets/credentials/{slug}/edit',
            name='/secrets/credentials/<slug>/edit',
            catch_response=True,
        ) as response:
            try:
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

                pk: str = cast(
                    str,
                    cast(Tag, soup.find('input', attrs={'name': 'pk'})).get('value'),
                )

                response.success()

            except AttributeError:
                response.failure(f'Page not correctly loaded: {response.status_code=}')
                return

        with self.client.post(
            f'/secrets/credentials/{slug}/edit',
            CredentialContract(
                csrfmiddlewaretoken=self.csrftoken,
                pk=pk,
                name=name,
                service=service_uuid,
                slug=slug,
                third_party_login=False,
                third_party_login_name='-----',
                login=self.F.user_name().strip(),
                password=self.F.password().strip(),
            ),
            name='/secrets/credentials/<slug>/edit',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/credentials/{slug}/edit',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and slug in response.headers.get('Location', ''):
                response.success()
            else:
                response.failure(
                    f'Update failure: status code = {response.status_code}'
                )
        # ==================

        # ===== DELETE =====
        self.client.get(
            f'/secrets/credentials/{slug}/delete',
            name='/secrets/credentials/<slug>/delete',
        )

        with self.client.post(
            f'/secrets/credentials/{slug}/delete',
            {'csrfmiddlewaretoken': self.csrftoken},
            name='/secrets/credentials/<slug>/delete',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/credentials/{slug}/delete',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and '/secrets/credentials/' == response.headers.get(
                'Location', ''
            ):
                response.success()
            else:
                response.failure(
                    f'Create failure: status code = {response.status_code}'
                )
        # ==================

    @task
    def card_crud(self) -> None:
        """Flow for LoginCredential CRUD"""

        # ===== CREATE =====
        with self.client.get(
            '/secrets/payment-cards/new',
            name='/secrets/payment-cards/new',
            catch_response=True,
        ) as response:
            try:
                self.csrftoken: str = response.cookies['crosstoken'].strip()

                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

                card_type_options = cast(
                    Tag, soup.find('select', attrs={'name': 'card_type'})
                ).find_all('option')
                valid_card_type_options = [
                    opt for opt in card_type_options if opt.get('value')
                ]

                chosen_card_type = choice(valid_card_type_options)

                card_type_uuid: str = str(chosen_card_type.get('value')).strip()

                bank_options = cast(
                    Tag, soup.find('select', attrs={'name': 'bank'})
                ).find_all('option')
                valid_bank_options = [opt for opt in bank_options if opt.get('value')]

                chosen_bank = choice(valid_bank_options)

                bank_uuid: str = str(chosen_bank.get('value')).strip()
                bank_name: str = chosen_bank.text.strip()

                brand_options = cast(
                    Tag, soup.find('select', attrs={'name': 'brand'})
                ).find_all('option')
                valid_brand_options = [opt for opt in brand_options if opt.get('value')]

                chosen_brand = choice(valid_brand_options)

                brand_uuid: str = str(chosen_brand.get('value')).strip()

                name: str = self.F.sentence(nb_words=4)[:10].strip()

                slug: str = slugify(f'{bank_name} {name}').strip()

                response.success()

            except AttributeError:
                response.failure(f'Page not correctly loaded: {response.status_code=}')
                return

        with self.client.post(
            '/secrets/payment-cards/new',
            CardContract(
                csrfmiddlewaretoken=self.csrftoken,
                pk=None,
                name=name,
                owners_name=self.F.name(),
                card_type=card_type_uuid,
                number=self.F.numerify('################'),
                expiration_0=randint(1, 12),
                expiration_1=randint(2030, 2050),
                cvv=self.F.numerify('###'),
                bank=bank_uuid,
                brand=brand_uuid,
                branch=self.F.numerify('###'),
                account=self.F.numerify('###'),
                password=self.F.numerify('####'),
                slug=slug,
            ),
            name='/secrets/payment-cards/new',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/payment-cards/new',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and slug in response.headers.get('Location', ''):
                response.success()
            else:
                response.failure(
                    f'Create failure: status code = {response.status_code}'
                )
        # ==================

        # ====== READ ======
        with self.client.get(
            f'/secrets/payment-cards/{slug}',
            name='/secrets/payment-cards/<slug>',
            catch_response=True,
        ) as response:
            if bank_name in response.text and (
                response.status_code == 200 or response.is_redirect
            ):
                response.success()
            else:
                response.failure(f'Read failure: status code = {response.status_code}')
        # ==================

        # ===== UPDATE =====
        with self.client.get(
            f'/secrets/payment-cards/{slug}/edit',
            name='/secrets/payment-cards/<slug>/edit',
            catch_response=True,
        ) as response:
            try:
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

                pk: str = cast(
                    str,
                    cast(Tag, soup.find('input', attrs={'name': 'pk'})).get('value'),
                )

                response.success()

            except AttributeError:
                response.failure(f'Page not correctly loaded: {response.status_code=}')
                return

        with self.client.post(
            f'/secrets/payment-cards/{slug}/edit',
            CardContract(
                csrfmiddlewaretoken=self.csrftoken,
                pk=pk,
                name=name,
                owners_name=self.F.name(),
                card_type=card_type_uuid,
                number=self.F.numerify('################'),
                expiration_0=randint(1, 12),
                expiration_1=randint(2030, 2050),
                cvv=self.F.numerify('###'),
                bank=bank_uuid,
                brand=brand_uuid,
                branch=self.F.numerify('###'),
                account=self.F.numerify('###'),
                password=self.F.numerify('####'),
                slug=slug,
            ),
            name='/secrets/payment-cards/<slug>/edit',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/payment-cards/{slug}/edit',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and slug in response.headers.get('Location', ''):
                response.success()
            else:
                response.failure(
                    f'Update failure: status code = {response.status_code}'
                )
        # ==================

        # ===== DELETE =====
        self.client.get(
            f'/secrets/payment-cards/{slug}/delete',
            name='/secrets/payment-cards/<slug>/delete',
        )

        with self.client.post(
            f'/secrets/payment-cards/{slug}/delete',
            {'csrfmiddlewaretoken': self.csrftoken},
            name='/secrets/payment-cards/<slug>/delete',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/payment-cards/{slug}/delete',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if (
                response.is_redirect
                and '/secrets/payment-cards/' == response.headers.get('Location', '')
            ):
                response.success()
            else:
                response.failure(
                    f'Create failure: status code = {response.status_code}'
                )
        # ==================

    @task
    def note_crud(self) -> None:
        """Flow for SecurityNote CRUD"""

        # ===== CREATE =====
        with self.client.get(
            '/secrets/notes/new', name='/secrets/notes/new', catch_response=True
        ) as response:
            try:
                self.csrftoken: str = response.cookies['crosstoken'].strip()

                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

                note_type_options = cast(
                    Tag, soup.find('select', attrs={'name': 'note_type'})
                ).find_all('option')
                valid_note_type_options = [
                    opt for opt in note_type_options if opt.get('value')
                ]

                chosen_note_type = choice(valid_note_type_options)

                note_type_uuid: str = str(chosen_note_type.get('value')).strip()

                title: str = self.F.sentence(nb_words=4)[:10].strip()

                slug: str = slugify(title).strip()

                response.success()

            except AttributeError:
                response.failure(f'Page not correctly loaded: {response.status_code=}')
                return

        with self.client.post(
            '/secrets/notes/new',
            NoteContract(
                csrfmiddlewaretoken=self.csrftoken,
                pk=None,
                title=title,
                content=self.F.text(max_nb_chars=1000),
                note_type=note_type_uuid,
                slug=slug,
            ),
            name='/secrets/notes/new',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/notes/new',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and slug in response.headers.get('Location', ''):
                response.success()
            else:
                response.failure(
                    f'Create failure: status code = {response.status_code}'
                )
        # ==================

        # ====== READ ======
        with self.client.get(
            f'/secrets/notes/{slug}',
            name='/secrets/notes/<slug>',
            catch_response=True,
        ) as response:
            if title[len(title) // 2] in response.text and (
                response.status_code == 200 or response.is_redirect
            ):
                response.success()
            else:
                response.failure(f'Read failure: status code = {response.status_code}')
        # ==================

        # ===== UPDATE =====
        with self.client.get(
            f'/secrets/notes/{slug}/edit',
            name='/secrets/notes/<slug>/edit',
            catch_response=True,
        ) as response:
            try:
                soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

                pk: str = cast(
                    str,
                    cast(Tag, soup.find('input', attrs={'name': 'pk'})).get('value'),
                )

                response.success()

            except AttributeError:
                response.failure(f'Page not correctly loaded: {response.status_code=}')
                return

        with self.client.post(
            f'/secrets/notes/{slug}/edit',
            NoteContract(
                csrfmiddlewaretoken=self.csrftoken,
                pk=pk,
                title=title,
                content=self.F.text(max_nb_chars=1000),
                note_type=note_type_uuid,
                slug=slug,
            ),
            name='/secrets/notes/<slug>/edit',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/notes/{slug}/edit',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and slug in response.headers.get('Location', ''):
                response.success()
            else:
                response.failure(
                    f'Update failure: status code = {response.status_code}'
                )
        # ==================

        # ===== DELETE =====
        self.client.get(
            f'/secrets/notes/{slug}/delete',
            name='/secrets/notes/<slug>/delete',
        )

        with self.client.post(
            f'/secrets/notes/{slug}/delete',
            {'csrfmiddlewaretoken': self.csrftoken},
            name='/secrets/notes/<slug>/delete',
            headers={
                'X-CSRFToken': self.csrftoken,
                'Referer': f'{self.host}/secrets/notes/{slug}/delete',
            },
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.is_redirect and '/secrets/notes/' == response.headers.get(
                'Location', ''
            ):
                response.success()
            else:
                response.failure(
                    f'Create failure: status code = {response.status_code}'
                )
        # ==================
