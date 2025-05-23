from account.models import User
from django.contrib.auth import get_user
from django.core import mail
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from secret.models import PaymentCard, LoginCredential, SecurityNote
from secret.month.models import Month
from utils import (
    create_scenarios,
    send_email_activate_account_completed,
    send_email_activation_account_token,
)


class BaseMailTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            passphrase='passphrase',
            email='user@email.com',
        )


class ExportSecretsViewTestCase(BaseMailTestCase):
    def test_GET_anonymous_user_no_argument(self) -> None:
        """GET /enviar-email/exportar-segredos/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('mail:export_secrets_no_argument'),
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets_no_argument'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user_no_argument(self) -> None:
        """GET /enviar-email/exportar-segredos/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets_no_argument'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_invalid_secret(self) -> None:
        """GET /enviar-email/exportar-segredos/<Any> | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('mail:export_secrets', args=['invalid']),
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user_invalid_secret(self) -> None:
        """GET /enviar-email/exportar-segredos/<Any> | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user_no_secret(self) -> None:
        """GET /enviar-email/exportar-segredos/<Credenciais | Cartões | Anotações> | authenticated user | no secret"""  # noqa: E501

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        secrets: list[tuple[str, str]] = [
            ('Credenciais', 'secret:credential_list_view'),
            ('Cartões', 'secret:card_list_view'),
            ('Anotações', 'secret:note_list_view'),
        ]

        for secret, url in secrets:
            with self.subTest(secret=secret):
                res: HttpResponse = self.client.get(
                    reverse('mail:export_secrets', args=[secret])
                )

                self.assertEqual(res.status_code, 302)
                self.assertRedirects(res, reverse(url))

                res: HttpResponse = self.client.get(
                    reverse('mail:export_secrets', args=[secret]), follow=True
                )

                self.assertEqual(res.status_code, 200)
                self.assertTemplateUsed(res, 'secret/list_view.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user_credential(self) -> None:
        """GET /enviar-email/exportar-segredos/Credenciais | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        LoginCredential.objects.create(
            owner=self.user,
            service='google--',
            name='Personal Main Account',
            slug='google--personal-main-account',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gcom',
            password='ilovemenotyou',
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Credenciais'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:credential_list_view'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Credenciais']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
        self.assertEqual(
            mail.outbox[-1].body,
            'Aqui estão seus segredos armazenados em "Credenciais" no sWarden.\n\nEquipe sWarden',  # noqa: E501
        )

    def test_GET_authenticated_user_card(self) -> None:
        """GET /enviar-email/exportar-segredos/Cartões | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card',
            card_type='deb',
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank='nubank--',
            brand='mastercard--',
            slug='nubank--personal-main-card',
            owners_name='TEST USER',
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Cartões'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:card_list_view'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Cartões']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
        self.assertEqual(
            mail.outbox[-1].body,
            'Aqui estão seus segredos armazenados em "Cartões" no sWarden.\n\nEquipe sWarden',  # noqa: E501
        )

    def test_GET_authenticated_user_note(self) -> None:
        """GET /enviar-email/exportar-segredos/Anotações | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            content='Just draw an apple tree and erase the tree.',
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Anotações'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:note_list_view'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Anotações']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['user@email.com'])
        self.assertEqual(
            mail.outbox[-1].body,
            'Aqui estão seus segredos armazenados em "Anotações" no sWarden.\n\nEquipe sWarden',  # noqa: E501
        )


class EmailActivationAccountTokenTestCase(BaseMailTestCase):
    def test_ideal(self) -> None:
        """
        send_email_activation_account_token(
            domain: str,
            user: User,
            password: str
        )
        """

        self.assertIsNone(
            send_email_activation_account_token('domain', self.user, 'password')
        )
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
            send_email_activation_account_token(500, self.user, 'password')  # type: ignore

    def test_wrong_type_user_arg(self) -> None:
        """
        send_email_activation_account_token(
            domain: str,
            user: not User,
            password: str
        )
        """

        with self.assertRaises(TypeError):
            send_email_activation_account_token('domain', 'self.user', 'password')  # type: ignore

    def test_wrong_type_password_arg(self) -> None:
        """
        send_email_activation_account_token(
            domain: str,
            user: User,
            password: not str
        )
        """

        with self.assertRaises(TypeError):
            send_email_activation_account_token('domain', self.user, 500)  # type: ignore

    def test_missing_args(self) -> None:
        """
        send_email_activation_account_token(
            domain: str | None,
            user: User | None,
            password: str | None
        )
        """

        params: list[dict[str, str | User]] = [
            {'domain': 'domain'},
            {'user': self.user},
            {'password': 'password'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises(TypeError):
                    send_email_activation_account_token(**scenario)


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
            send_email_activate_account_completed(4)  # type: ignore

    def test_function_behavior_no_argument(self) -> None:
        """send_email_activate_account_completed(user_email: str | None)"""

        with self.assertRaises(TypeError):
            send_email_activate_account_completed()  # type: ignore


class WakeDatabaseViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            passphrase='passphrase',
            email='user@email.com',
        )

        self.ENDPOINT: str = reverse('mail:wake')

    def test_GET_anonymous_user(self) -> None:
        """GET /enviar-email/wake | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.ENDPOINT)

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /enviar-email/wake | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.get(self.ENDPOINT)

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user(self) -> None:
        """POST /enviar-email/wake | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            self.ENDPOINT, {'DATA': 'HERE'}, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Logged user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self) -> None:
        """POST /enviar-email/wake | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.post(
            self.ENDPOINT, {'DATA': 'HERE'}, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_return_values(self) -> None:
        """POST /enviar-email/wake | return values based on num of reqs"""

        for i in range(1, 17):
            with self.subTest(i=i):
                res: HttpResponse = self.client.get(self.ENDPOINT)
                self.assertEqual(int(res.content), i % 4)
