from account.models import User
from django.contrib.auth import get_user
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from secret.models import Card, LoginCredential, SecurityNote
from secret.month.models import Month
from secret.views import EMPTY_POST_MSG, FEEDBACK_MSG


class SecretIndexViewTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /segredo/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('secret:index'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('account:login') + '?next=' + reverse('secret:index')
        )

        res: HttpResponse = self.client.get(reverse('secret:index'), follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /segredo/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


# --------------------------------------------------
# LoginCredential CRUD View Testing
# --------------------------------------------------


class BaseLoginCredentialTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

        LoginCredential.objects.create(
            owner=self.user,
            service='google--',
            name='Personal Main Account',
            slug='google--personal-main-account',
            thirdy_party_login=False,
            thirdy_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        )

        LoginCredential.objects.create(
            owner=self.user,
            service='steam--',
            name='Little Fries',
            slug='steam--little-fries',
            thirdy_party_login=True,
            thirdy_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        )


class LoginCredentialCreateViewsTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /segredo/credenciais/nova | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('secret:credential_create_view'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_create_view'),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:credential_create_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /segredo/credenciais/nova | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:credential_create_view'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Credencial')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /segredo/credenciais/nova | anonymous user | empty form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'), {}
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_create_view'),
        )

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'),
            {},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /segredo/credenciais/nova | authenticated user | empty form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'),
            {},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Credencial')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """POST /segredo/credenciais/nova | anonymous user | existent secret slug"""

        cred_data: dict = {
            'owner': self.user,
            'service': 'google--',
            'name': 'Personal Main Account',
            'slug': 'google--personal-main-account',
            'thirdy_party_login': False,
            'thirdy_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'), cred_data
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_create_view'),
        )

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'),
            cred_data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /segredo/credenciais/nova | authenticated user | empty form"""

        cred_data: dict = {
            'owner': self.user,
            'service': 'google--',
            'name': 'Personal Main Account',
            'slug': 'google--personal-main-account',
            'thirdy_party_login': False,
            'thirdy_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'),
            cred_data,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Credencial')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /segredo/credenciais/nova | authenticated user | valid form"""

        cred_data: dict = {
            'owner': self.user,
            'service': 'google--',
            'name': 'Another Personal Main Account',
            'slug': 'google--another-personal-main-account',
            'thirdy_party_login': False,
            'thirdy_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:credential_create_view'),
            cred_data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Credencial')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class LoginCredentialListViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /segredo/credenciais/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('secret:credential_list_view'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_list_view'),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:credential_list_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /segredo/credenciais/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:credential_list_view'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertIn('object_list', res.context.keys())  # type: ignore
        self.assertEqual(len(res.context['object_list']), 2)
        self.assertIn('model_name', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model_name'], 'Credenciais')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class LoginCredentialDetailViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /segredo/credenciais/<slug:slug> | anonymous user"""

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'google--personal-main-account'},
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'google--personal-main-account'},
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'google--personal-main-account'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /segredo/credenciais/<slug:slug> | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'google--personal-main-account'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Credential/detail_view.html')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='google--personal-main-account'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'lasagna--double-pizza'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class LoginCredentialUpdateViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /segredo/credenciais/<slug:slug>/editar | anonymous user"""

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'google--personal-main-account'},
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'google--personal-main-account'},
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'google--personal-main-account'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /segredo/credenciais/<slug:slug>/editar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'google--personal-main-account'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Edição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='google--personal-main-account'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'lasagna--double-pizza'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class LoginCredentialDeleteViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /segredo/credenciais/<slug:slug>/deletar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'google--personal-main-account'},
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'google--personal-main-account'},
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'google--personal-main-account'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /segredo/credenciais/<slug:slug>/deletar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'google--personal-main-account'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Exclusão')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='google--personal-main-account'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'lasagna--double-pizza'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


# --------------------------------------------------
# Card CRUD View Testing
# --------------------------------------------------


class BaseCardTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

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


class CardCreateViewsTestCase(BaseCardTestCase):
    def test_GET_create_anonymous_user(self) -> None:
        """GET /segredo/cartoes/novo | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('secret:card_create_view'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:card_create_view'),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:card_create_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_create_authenticated_user(self) -> None:
        """GET /segredo/cartoes/novo | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:card_create_view'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Cartão')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /segredo/cartoes/novo | anonymous user | empty form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {})

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:card_create_view'),
        )

        res: HttpResponse = self.client.post(
            reverse('secret:card_create_view'),
            {},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /segredo/cartoes/novo | authenticated user | empty form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:card_create_view'),
            {},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Cartão')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """GET /segredo/cartoes/novo | anonymous user | existent secret slug"""

        card_data: dict = {
            'owner': self.user,
            'name': 'Personal Main Card',
            'card_type': 'deb',
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': 'nubank--',
            'brand': 'mastercard--',
            'slug': 'nubank--personal-main-card',
            'owners_name': 'TEST USER',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('secret:card_create_view'), card_data
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:card_create_view'),
        )

        res: HttpResponse = self.client.post(
            reverse('secret:card_create_view'),
            card_data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /segredo/cartoes/novo | authenticated user | empty form"""

        card_data: dict = {
            'owner': self.user,
            'name': 'Personal Main Card',
            'card_type': 'deb',
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': 'nubank--',
            'brand': 'mastercard--',
            'slug': 'nubank--personal-main-card',
            'owners_name': 'TEST USER',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:card_create_view'),
            card_data,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Cartão')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /segredo/cartoes/novo | authenticated user | valid form"""

        card_data: dict = {
            'owner': self.user,
            'name': 'Another Personal Main Card',
            'card_type': 'deb',
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': 'nubank--',
            'brand': 'mastercard--',
            'slug': 'nubank--another-personal-main-card',
            'owners_name': 'TEST USER',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:card_create_view'),
            card_data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Cartão')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class CardListViewTestCase(BaseCardTestCase):
    def test_GET_list_anonymous_user(self) -> None:
        """GET /segredo/cartoes/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('secret:card_list_view'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('account:login') + '?next=' + reverse('secret:card_list_view')
        )

        res: HttpResponse = self.client.get(
            reverse('secret:card_list_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_list_authenticated_user(self) -> None:
        """GET /segredo/cartoes/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:card_list_view'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertIn('object_list', res.context.keys())  # type: ignore
        self.assertEqual(len(res.context['object_list']), 1)
        self.assertIn('model_name', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model_name'], 'Cartões')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class CardDetailViewTestCase(BaseCardTestCase):
    def test_GET_detail_anonymous_user(self) -> None:
        """GET /segredo/cartoes/<slug:slug> | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_detail_authenticated_user(self) -> None:
        """GET /segredo/cartoes/<slug:slug> | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Card/detail_view.html')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            Card.objects.get(
                owner=User.objects.first(), slug='nubank--personal-main-card'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:card_detail_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class CardUpdateViewTestCase(BaseCardTestCase):
    def test_GET_update_anonymous_user(self) -> None:
        """GET /segredo/cartoes/<slug:slug>/editar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_update_authenticated_user(self) -> None:
        """GET /segredo/cartoes/<slug:slug>/editar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Edição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            Card.objects.get(
                owner=User.objects.first(), slug='nubank--personal-main-card'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:card_update_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class CardDeleteViewTestCase(BaseCardTestCase):
    def test_GET_delete_anonymous_user(self) -> None:
        """GET /segredo/cartoes/<slug:slug>/deletar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}
            ),
        )

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_delete_authenticated_user(self) -> None:
        """GET /segredo/cartoes/<slug:slug>/deletar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse(
                'secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Exclusão')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            Card.objects.get(
                owner=User.objects.first(), slug='nubank--personal-main-card'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:card_delete_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


# --------------------------------------------------
# SecurityNote CRUD View Testing
# --------------------------------------------------


class BaseSecurityNoteTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

        SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            content='Just draw an apple tree and erase the tree.',
        )


class SecurityNoteCreateViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_create_anonymous_user(self) -> None:
        """GET /segredo/anotacoes/novo | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('secret:note_create_view'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:note_create_view'),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_create_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_create_authenticated_user(self) -> None:
        """GET /segredo/anotacoes/novo | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:note_create_view'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Anotação')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /segredo/anotacoes/novo | anonymous user | empty form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {})

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:note_create_view'),
        )

        res: HttpResponse = self.client.post(
            reverse('secret:note_create_view'),
            {},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /segredo/anotacoes/novo | authenticated user | empty form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:note_create_view'),
            {},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Anotação')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """GET /segredo/anotacoes/novo | anonymous user | existent secret slug"""

        note_data: dict = {
            'owner': self.user,
            'title': 'How to draw an apple',
            'slug': 'how-to-draw-an-apple',
            'content': 'Just draw an apple tree and erase the tree.',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('secret:note_create_view'), note_data
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:note_create_view'),
        )

        res: HttpResponse = self.client.post(
            reverse('secret:note_create_view'),
            note_data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /segredo/anotacoes/novo | authenticated user | empty form"""

        note_data: dict = {
            'owner': self.user,
            'title': 'How to draw an apple',
            'slug': 'how-to-draw-an-apple',
            'content': 'Just draw an apple tree and erase the tree.',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:note_create_view'),
            note_data,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Anotação')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /segredo/anotacoes/novo | authenticated user | valid form"""

        note_data: dict = {
            'owner': self.user,
            'title': 'How not to draw an apple',
            'slug': 'how-not-to-draw-an-apple',
            'content': 'Just not draw an apple tree and erase the tree.',
        }

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('secret:note_create_view'),
            note_data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Anotação')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class SecurityNoteListViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_list_anonymous_user(self) -> None:
        """GET /segredo/anotacoes/ | anonymous user"""

        res: HttpResponse = self.client.get(reverse('secret:note_list_view'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('account:login') + '?next=' + reverse('secret:note_list_view')
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_list_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_list_authenticated_user(self) -> None:
        """GET /segredo/anotacoes/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('secret:note_list_view'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertIn('object_list', res.context.keys())  # type: ignore
        self.assertEqual(len(res.context['object_list']), 1)
        self.assertIn('model_name', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model_name'], 'Anotações')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class SecurityNoteDetailViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_detail_anonymous_user(self) -> None:
        """GET /segredo/anotacoes/<slug:slug> | anonymous user"""

        res: HttpResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_detail_authenticated_user(self) -> None:
        """GET /segredo/anotacoes/<slug:slug> | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Note/detail_view.html')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class SecurityNoteUpdateViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_update_anonymous_user(self) -> None:
        """GET /segredo/anotacoes/<slug:slug>/editar | anonymous user"""

        res: HttpResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_update_authenticated_user(self) -> None:
        """GET /segredo/anotacoes/<slug:slug>/editar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Edição')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class SecurityNoteDeleteViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_delete_anonymous_user(self) -> None:
        """GET /segredo/anotacoes/<slug:slug>/deletar | anonymous user"""

        res: HttpResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_delete_authenticated_user(self) -> None:
        """GET /segredo/anotacoes/<slug:slug>/deletar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertIn('action', res.context.keys())  # type: ignore
        self.assertEqual(res.context['action'], 'Exclusão')
        self.assertIn('model', res.context.keys())  # type: ignore
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertIn('object', res.context.keys())  # type: ignore
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

        res: HttpResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
