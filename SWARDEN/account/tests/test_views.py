from typing import cast

from django.contrib.auth import get_user
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import ActivationAccountToken, User


class BaseAccountTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='password',
            email='user@email.com',
        )

        self.REGISTER_URL: str = reverse('account:register')
        self.LOGIN_URL: str = reverse('account:login')
        self.LOGOUT_URL: str = reverse('account:logout')


class RegisterViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /conta/registrar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /conta/registrar | anonymous user | invalid form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            self.REGISTER_URL, {'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_different_passwords(self) -> None:
        """POST /conta/registrar | anonymous user | different passwords"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str] = {
            'username': 'username',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'another@example.com',
            'password': '12345678',
            'password2': '11223344',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_existing_register(self) -> None:
        """POST /conta/registrar | anonymous user | register already exists"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str] = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@example.com',
            'password': 'password',
            'password2': 'password',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_empty_names(self) -> None:
        """POST /conta/registrar | anonymous user | empty first_name and/or last_name"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str | None] = {
            'username': 'username',
            'first_name': '',
            'last_name': 'last',
            'email': 'email@example.com',
            'password': 'password',
            'password2': 'password',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_valid_form(self) -> None:
        """POST /conta/registrar | anonymous user | valid form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        post_data: dict[str, str] = {
            'username': 'username',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'another@example.com',
            'password': 'password',
            'password2': 'password',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /conta/registrar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(self.REGISTER_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')


class ActivateAccountViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user_no_parameter(self) -> None:
        """GET /conta/ativar/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_parameter'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_missing_token(self) -> None:
        """GET /conta/ativar/<Any> | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_token', args=['404'])
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_token', args=['404']), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_invalid_uidb64(self) -> None:
        """GET /conta/ativar/<uidb64>/<token> | anonymous user | invalid uidb64"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=['404', 'x' * 64])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_inexistent_token(self) -> None:
        """GET /conta/ativar/<uidb64>/<token> | anonymous user | inexistent token"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        user: User = cast(User, User.objects.first())
        user_pk: str = user.pk
        uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, 'x' * 64])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user(self) -> None:
        """GET /conta/ativar/<uidb64>/<token> | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        user: User = cast(User, User.objects.first())

        uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /conta/ativar/<uidb64>/<token> | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        user: User = cast(User, User.objects.first())

        uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)


class LoginViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /conta/entrar | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {'username': 'user', 'password': 'password', 'email': 'email@example.com'},
            follow=True,
        )
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_invalid_form(self) -> None:
        """GET /conta/entrar | anonymous user | invalid form"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {'username': 'user', 'email': 'email@example.com'},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_user_is_None(self) -> None:
        """GET /conta/entrar | anonymous user | user is None"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {
                'username': 'fake_user',
                'password': 'password',
                'email': 'email@example.com',
            },
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /conta/entrar | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(self.LOGIN_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')


class LogoutViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /conta/sair | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGOUT_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.LOGIN_URL + '?next=' + self.LOGOUT_URL)

        res: HttpResponse = self.client.get(self.LOGOUT_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user(self) -> None:
        """GET /conta/sair | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGOUT_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/logout.html')
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user(self) -> None:
        """POST /conta/sair | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(self.LOGOUT_URL)

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertEqual(res.status_code, 302)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(self.LOGOUT_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
