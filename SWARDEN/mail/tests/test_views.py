from django.http import HttpResponse
from django.test import TestCase
from django.core import mail
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user
from django.urls import reverse

from account.models import User
from secret.models import LoginCredential, Card, SecurityNote
from secret.month.models import Month
from utils import (
    create_scenarios,
    send_email_activation_account_token,
    send_email_activate_account_completed,
)


class MailViewTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='user',
            password='password',
            email='email@example.com',
        )

    def test_export_secrets_no_argument_view_behavior_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))

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

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_export_secrets_no_argument_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('mail:export_secrets_no_argument'))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets_no_argument'), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_export_secrets_invalid_argument_view_behavior_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/<Any>" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid'])
        )

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

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_export_secrets_invalid_argument_view_behavior_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/<Any>" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid'])
        )

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['invalid']), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_export_secrets_argument_with_no_secret_view_behavior_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/<Credenciais | Cartões | Anotações>" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

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

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_export_secrets_for_credential_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/Credenciais" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        LoginCredential.objects.create(
            owner=self.user,
            service='google--',
            name='Personal Main Account',
            slug='google--personal-main-account',
            thirdy_party_login=False,
            thirdy_party_login_name='-----',
            login='night_monkey123@gcom',
            password='ilovemenotyou',
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Credenciais'])
        )

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:credential_list_view'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Credenciais']), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['email@example.com'])
        self.assertEqual(
            mail.outbox[-1].body,
            'Aqui estão seus segredos armazenados em "Credenciais" no sWarden.\n\n\nEquipe sWarden',
        )

    def test_export_secrets_for_card_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/Cartões" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        Card.objects.create(
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

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:card_list_view'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Cartões']), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['email@example.com'])
        self.assertEqual(
            mail.outbox[-1].body,
            'Aqui estão seus segredos armazenados em "Cartões" no sWarden.\n\n\nEquipe sWarden',
        )

    def test_export_secrets_for_note_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/enviar-email/exportar-segredos/Anotações" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            content='Just draw an apple tree and erase the tree.',
        )

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Anotações'])
        )

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('secret:note_list_view'))

        res: HttpResponse = self.client.get(
            reverse('mail:export_secrets', args=['Anotações']), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[-1].subject, 'Exportação de Segredos | sWarden')
        self.assertEqual(mail.outbox[-1].to, ['email@example.com'])
        self.assertEqual(
            mail.outbox[-1].body,
            'Aqui estão seus segredos armazenados em "Anotações" no sWarden.\n\n\nEquipe sWarden',
        )


class EmailActivationAccountTokenTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User(
            username='username',
            password='password',
            email='email@example.com',
        )

    def test_fuction_behavior_ideal_scenario(self) -> None:
        """Tests function behavior when calling with expected arguments"""

        self.assertIsNone(
            send_email_activation_account_token('domain', self.user, 'password')
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[-1].subject, 'Ativação de Conta | sWarden')
        self.assertTrue(mail.outbox[-1].to, ['email@example.com'])

    def test_fuction_behavior_invalid_User_scenario(self) -> None:
        """Tests function behavior when user is an invalid instance"""

        user: User = User()

        with self.assertRaises(ValidationError):
            send_email_activation_account_token('domain', user, 'password')

    def test_fuction_behavior_wrong_type_for_domain_arg(self) -> None:
        """Tests function behavior when type(domain) != str"""

        with self.assertRaises(TypeError):
            send_email_activation_account_token(500, self.user, 'password')

    def test_fuction_behavior_wrong_type_for_user_arg(self) -> None:
        """Tests function behavior when type(user) != User"""

        with self.assertRaises(TypeError):
            send_email_activation_account_token('domain', 'self.user', 'password')

    def test_fuction_behavior_wrong_type_for_password_arg(self) -> None:
        """Tests function behavior when type(password) != str"""

        with self.assertRaises(TypeError):
            send_email_activation_account_token('domain', self.user, 500)

    def test_fuction_behavior_missing_args_scenario(self) -> None:
        """Tests function behavior when missing args"""

        params: list[dict[str, str | User]] = [
            {'domain': 'domain'},
            {'user': self.user},
            {'password': 'password'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises(TypeError):
                    send_email_activation_account_token(**scenario)


class EmailActivationAccountDoneTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User(
            username='username',
            password='password',
            email='email@example.com',
        )

    def test_fuction_behavior_ideal_scenario(self) -> None:
        """Tests function behavior when calling with expected arguments"""

        self.assertIsNone(send_email_activate_account_completed('email@example.com'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(mail.outbox[-1].subject, 'Ativação de Conta | sWarden')
        self.assertTrue(mail.outbox[-1].to, ['email@example.com'])

    def test_fuction_behavior_invalid_email_scenario(self) -> None:
        """Tests function behavior when invalid user_email"""

        with self.assertRaises(TypeError):
            send_email_activate_account_completed(4)

    def test_function_behavior_no_argument(self) -> None:
        """Tests function behavior when missing arg user_email"""

        with self.assertRaises(TypeError):
            send_email_activate_account_completed()
