
# File: `test_views.py`
Path: `SWARDEN.mail.tests`



---

## Imports

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```

### `#!py import get_user`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import get_user
    ```

### `#!py import mail`

Path: `#!py django.core`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core import mail
    ```

### `#!py import ValidationError`

Path: `#!py django.core.exceptions`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.exceptions import ValidationError
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import TestCase`

Path: `#!py django.test`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.test import TestCase
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.urls import reverse
    ```

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import SecurityNote
    ```

### `#!py import Month`

Path: `#!py secret.month.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.month.models import Month
    ```

### `#!py import create_scenarios`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import create_scenarios
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



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class BaseMailTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class BaseMailTestCase(TestCase):

        def setUp(self) -> None:
            self.user: User = User.objects.create_user(username='user', password='password', email='user@email.com')
    ```

### `#!py class ExportSecretsViewTestCase`

Parents: `BaseMailTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class ExportSecretsViewTestCase(BaseMailTestCase):

        def test_GET_anonymous_user_no_argument(self) -> None:
            """GET /enviar-email/exportar-segredos/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('mail:export_secrets_no_argument'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user_no_argument(self) -> None:
            """GET /enviar-email/exportar-segredos/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('home:index'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_invalid_secret(self) -> None:
            """GET /enviar-email/exportar-segredos/<Any> | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('mail:export_secrets', args=['invalid']))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user_invalid_secret(self) -> None:
            """GET /enviar-email/exportar-segredos/<Any> | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('home:index'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user_no_secret(self) -> None:
            """GET /enviar-email/exportar-segredos/<Credenciais | Cartões | Anotações> | authenticated user | no secret"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            secrets: list[tuple[str, str]] = [('Credenciais', 'secret:credential_list_view'), ('Cartões', 'secret:card_list_view'), ('Anotações', 'secret:note_list_view')]
            for (secret, url) in secrets:
                with self.subTest(secret=secret):
                    res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=[secret]))
                    self.assertEqual(res.status_code, 302)
                    self.assertRedirects(res, reverse(url))
                    res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=[secret]), follow=True)
                    self.assertEqual(res.status_code, 200)
                    self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user_credential(self) -> None:
            """GET /enviar-email/exportar-segredos/Credenciais | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            LoginCredential.objects.create(owner=self.user, service='google--', name='Personal Main Account', slug='google--personal-main-account', third_party_login=False, third_party_login_name='-----', login='night_monkey123@gcom', password='ilovemenotyou')
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Credenciais']))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('secret:credential_list_view'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Credenciais']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
            self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
            self.assertEqual(mail.outbox[-1].body, 'Aqui estão seus segredos armazenados em "Credenciais" no sWarden.\n\nEquipe sWarden')

        def test_GET_authenticated_user_card(self) -> None:
            """GET /enviar-email/exportar-segredos/Cartões | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            Card.objects.create(owner=self.user, name='Personal Main Card', card_type='deb', number='4002892240028922', expiration=Month(2028, 11), cvv='113', bank='nubank--', brand='mastercard--', slug='nubank--personal-main-card', owners_name='TEST USER')
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Cartões']))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('secret:card_list_view'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Cartões']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
            self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
            self.assertEqual(mail.outbox[-1].body, 'Aqui estão seus segredos armazenados em "Cartões" no sWarden.\n\nEquipe sWarden')

        def test_GET_authenticated_user_note(self) -> None:
            """GET /enviar-email/exportar-segredos/Anotações | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            SecurityNote.objects.create(owner=self.user, title='How to draw an apple', slug='how-to-draw-an-apple', content='Just draw an apple tree and erase the tree.')
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Anotações']))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('secret:note_list_view'))
            res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Anotações']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
            self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
            self.assertEqual(mail.outbox[-1].body, 'Aqui estão seus segredos armazenados em "Anotações" no sWarden.\n\nEquipe sWarden')
    ```

### `#!py class EmailActivationAccountTokenTestCase`

Parents: `BaseMailTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class EmailActivationAccountTokenTestCase(BaseMailTestCase):

        def test_ideal(self) -> None:
            """
            send_email_activation_account_token(
                domain: str,
                user: User,
                password: str
            )
            """
            self.assertIsNone(send_email_activation_account_token('domain', self.user, 'password'))
            self.assertEqual(len(mail.outbox), 1)
            self.assertTrue(mail.outbox[-1].subject, 'Ativação de Conta | sWarden')
            self.assertTrue(mail.outbox[-1].to, ['user@email.com'])

        def test_invalid_User(self) -> None:
            """
            send_email_activation_account_token(
                domain: str,
                user: User,
                password: str
            )
            """
            user: User = User()
            with self.assertRaises(ValidationError):
                send_email_activation_account_token('domain', user, 'password')

        def test_wrong_type_domain_arg(self) -> None:
            """
            send_email_activation_account_token(
                domain: not str,
                user: User,
                password: str
            )
            """
            with self.assertRaises(TypeError):
                send_email_activation_account_token(500, self.user, 'password')

        def test_wrong_type_user_arg(self) -> None:
            """
            send_email_activation_account_token(
                domain: str,
                user: not User,
                password: str
            )
            """
            with self.assertRaises(TypeError):
                send_email_activation_account_token('domain', 'self.user', 'password')

        def test_wrong_type_password_arg(self) -> None:
            """
            send_email_activation_account_token(
                domain: str,
                user: User,
                password: not str
            )
            """
            with self.assertRaises(TypeError):
                send_email_activation_account_token('domain', self.user, 500)

        def test_missing_args(self) -> None:
            """
            send_email_activation_account_token(
                domain: str | None,
                user: User | None,
                password: str | None
            )
            """
            params: list[dict[str, str | User]] = [{'domain': 'domain'}, {'user': self.user}, {'password': 'password'}]
            for (case, scenario) in create_scenarios(params):
                with self.subTest(scenario=case):
                    with self.assertRaises(TypeError):
                        send_email_activation_account_token(**scenario)
    ```

### `#!py class EmailActivationAccountDoneTestCase`

Parents: `BaseMailTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class EmailActivationAccountDoneTestCase(BaseMailTestCase):

        def test_ideal(self) -> None:
            """send_email_activate_account_completed(user_email: str)"""
            self.assertIsNone(send_email_activate_account_completed('user@email.com'))
            self.assertEqual(len(mail.outbox), 1)
            self.assertTrue(mail.outbox[-1].subject, 'Ativação de Conta | sWarden')
            self.assertTrue(mail.outbox[-1].to, ['user@email.com'])

        def test_invalid_email(self) -> None:
            """send_email_activate_account_completed(user_email: not str)"""
            with self.assertRaises(TypeError):
                send_email_activate_account_completed(4)

        def test_function_behavior_no_argument(self) -> None:
            """send_email_activate_account_completed(user_email: str | None)"""
            with self.assertRaises(TypeError):
                send_email_activate_account_completed()
    ```

### `#!py class WakeDatabaseViewTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class WakeDatabaseViewTestCase(TestCase):

        def setUp(self) -> None:
            self.user: User = User.objects.create_user(username='user', password='password', email='user@email.com')
            self.ENDPOINT: str = reverse('mail:wake')

        def test_GET_anonymous_user(self) -> None:
            """GET /enviar-email/wake | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.ENDPOINT)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /enviar-email/wake | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.get(self.ENDPOINT)
            self.assertEqual(res.status_code, 200)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user(self) -> None:
            """POST /enviar-email/wake | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(self.ENDPOINT, {'DATA': 'HERE'}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user(self) -> None:
            """POST /enviar-email/wake | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.post(self.ENDPOINT, {'DATA': 'HERE'}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_return_values(self) -> None:
            """POST /enviar-email/wake | return values based on num of reqs"""
            for i in range(1, 17):
                with self.subTest(i=i):
                    res: HttpResponse = self.client.get(self.ENDPOINT)
                    self.assertEqual(int(res.content), i % 4)
    ```



---

## Functions

### `#!py def setUp`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='user', password='password', email='user@email.com')
    ```

### `#!py def test_GET_anonymous_user_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user_no_argument(self) -> None:
        """GET /enviar-email/exportar-segredos/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('mail:export_secrets_no_argument'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_no_argument(self) -> None:
        """GET /enviar-email/exportar-segredos/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_invalid_secret`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user_invalid_secret(self) -> None:
        """GET /enviar-email/exportar-segredos/<Any> | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('mail:export_secrets', args=['invalid']))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user_invalid_secret`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_invalid_secret(self) -> None:
        """GET /enviar-email/exportar-segredos/<Any> | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['invalid']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user_no_secret`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_no_secret(self) -> None:
        """GET /enviar-email/exportar-segredos/<Credenciais | Cartões | Anotações> | authenticated user | no secret"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        secrets: list[tuple[str, str]] = [('Credenciais', 'secret:credential_list_view'), ('Cartões', 'secret:card_list_view'), ('Anotações', 'secret:note_list_view')]
        for (secret, url) in secrets:
            with self.subTest(secret=secret):
                res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=[secret]))
                self.assertEqual(res.status_code, 302)
                self.assertRedirects(res, reverse(url))
                res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=[secret]), follow=True)
                self.assertEqual(res.status_code, 200)
                self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user_credential`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_credential(self) -> None:
        """GET /enviar-email/exportar-segredos/Credenciais | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        LoginCredential.objects.create(owner=self.user, service='google--', name='Personal Main Account', slug='google--personal-main-account', third_party_login=False, third_party_login_name='-----', login='night_monkey123@gcom', password='ilovemenotyou')
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Credenciais']))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:credential_list_view'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Credenciais']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
        self.assertEqual(mail.outbox[-1].body, 'Aqui estão seus segredos armazenados em "Credenciais" no sWarden.\n\nEquipe sWarden')
    ```

### `#!py def test_GET_authenticated_user_card`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_card(self) -> None:
        """GET /enviar-email/exportar-segredos/Cartões | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        Card.objects.create(owner=self.user, name='Personal Main Card', card_type='deb', number='4002892240028922', expiration=Month(2028, 11), cvv='113', bank='nubank--', brand='mastercard--', slug='nubank--personal-main-card', owners_name='TEST USER')
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Cartões']))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:card_list_view'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Cartões']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
        self.assertEqual(mail.outbox[-1].body, 'Aqui estão seus segredos armazenados em "Cartões" no sWarden.\n\nEquipe sWarden')
    ```

### `#!py def test_GET_authenticated_user_note`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_note(self) -> None:
        """GET /enviar-email/exportar-segredos/Anotações | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        SecurityNote.objects.create(owner=self.user, title='How to draw an apple', slug='how-to-draw-an-apple', content='Just draw an apple tree and erase the tree.')
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Anotações']))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:note_list_view'))
        res: HttpResponse = self.client.get(reverse('mail:export_secrets', args=['Anotações']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
        self.assertEqual(mail.outbox[-1].body, 'Aqui estão seus segredos armazenados em "Anotações" no sWarden.\n\nEquipe sWarden')
    ```

### `#!py def test_ideal`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_ideal(self) -> None:
        """
            send_email_activation_account_token(
                domain: str,
                user: User,
                password: str
            )
            """
        self.assertIsNone(send_email_activation_account_token('domain', self.user, 'password'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[-1].subject, 'Ativação de Conta | sWarden')
        self.assertTrue(mail.outbox[-1].to, ['user@email.com'])
    ```

### `#!py def test_invalid_User`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_invalid_User(self) -> None:
        """
            send_email_activation_account_token(
                domain: str,
                user: User,
                password: str
            )
            """
        user: User = User()
        with self.assertRaises(ValidationError):
            send_email_activation_account_token('domain', user, 'password')
    ```

### `#!py def test_wrong_type_domain_arg`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_wrong_type_domain_arg(self) -> None:
        """
            send_email_activation_account_token(
                domain: not str,
                user: User,
                password: str
            )
            """
        with self.assertRaises(TypeError):
            send_email_activation_account_token(500, self.user, 'password')
    ```

### `#!py def test_wrong_type_user_arg`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_wrong_type_user_arg(self) -> None:
        """
            send_email_activation_account_token(
                domain: str,
                user: not User,
                password: str
            )
            """
        with self.assertRaises(TypeError):
            send_email_activation_account_token('domain', 'self.user', 'password')
    ```

### `#!py def test_wrong_type_password_arg`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_wrong_type_password_arg(self) -> None:
        """
            send_email_activation_account_token(
                domain: str,
                user: User,
                password: not str
            )
            """
        with self.assertRaises(TypeError):
            send_email_activation_account_token('domain', self.user, 500)
    ```

### `#!py def test_missing_args`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_missing_args(self) -> None:
        """
            send_email_activation_account_token(
                domain: str | None,
                user: User | None,
                password: str | None
            )
            """
        params: list[dict[str, str | User]] = [{'domain': 'domain'}, {'user': self.user}, {'password': 'password'}]
        for (case, scenario) in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises(TypeError):
                    send_email_activation_account_token(**scenario)
    ```

### `#!py def test_ideal`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_ideal(self) -> None:
        """send_email_activate_account_completed(user_email: str)"""
        self.assertIsNone(send_email_activate_account_completed('user@email.com'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[-1].subject, 'Ativação de Conta | sWarden')
        self.assertTrue(mail.outbox[-1].to, ['user@email.com'])
    ```

### `#!py def test_invalid_email`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_invalid_email(self) -> None:
        """send_email_activate_account_completed(user_email: not str)"""
        with self.assertRaises(TypeError):
            send_email_activate_account_completed(4)
    ```

### `#!py def test_function_behavior_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_function_behavior_no_argument(self) -> None:
        """send_email_activate_account_completed(user_email: str | None)"""
        with self.assertRaises(TypeError):
            send_email_activate_account_completed()
    ```

### `#!py def setUp`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='user', password='password', email='user@email.com')
        self.ENDPOINT: str = reverse('mail:wake')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /enviar-email/wake | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /enviar-email/wake | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.get(self.ENDPOINT)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_anonymous_user(self) -> None:
        """POST /enviar-email/wake | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(self.ENDPOINT, {'DATA': 'HERE'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_authenticated_user(self) -> None:
        """POST /enviar-email/wake | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.post(self.ENDPOINT, {'DATA': 'HERE'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_return_values`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_return_values(self) -> None:
        """POST /enviar-email/wake | return values based on num of reqs"""
        for i in range(1, 17):
            with self.subTest(i=i):
                res: HttpResponse = self.client.get(self.ENDPOINT)
                self.assertEqual(int(res.content), i % 4)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
