from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import User, ActivationAccountToken


# Create your tests here.
class AccountViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='password',
            email='email@example.com',
        )

        self.REGISTER_URL: str = reverse('account:register')
        self.LOGIN_URL: str = reverse('account:login')
        self.LOGOUT_URL: str = reverse('account:logout')

    def test_register_view_behavior_for_not_logged_users(self) -> None:
        """Tests view behavior at "/conta/registrar" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_register_POST_view_behavior_for_not_logged_users_invalid_form(
        self,
    ) -> None:
        """Tests view behavior at POST "/conta/registrar" for logged not users with an invalid form"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            self.REGISTER_URL, {'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_register_POST_view_behavior_for_not_logged_users_invalid_password(
        self,
    ) -> None:
        """Tests view behavior at POST "/conta/registrar" for logged not users with invalid password"""

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

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_register_POST_view_behavior_for_not_logged_users_user_already_exists(
        self,
    ) -> None:
        """Tests view behavior at POST "/conta/registrar" for logged not users user already exists"""

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

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_register_POST_view_behavior_for_not_logged_users_valid_form(self) -> None:
        """Tests view behavior at POST "/conta/registrar" for logged not users with valid form"""

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

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_register_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/conta/registrar" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.REGISTER_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(self.REGISTER_URL, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_login_view_behavior_for_not_logged_users(self) -> None:
        """Tests view behavior at "/conta/entrar" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {'username': 'user', 'password': 'password', 'email': 'email@example.com'},
            follow=True,
        )

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_login_view_behavior_for_not_logged_users_invalid_form(self) -> None:
        """Tests view behavior at "/conta/entrar" for not logged users posting invalid form"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

        res: HttpResponse = self.client.post(
            self.LOGIN_URL,
            {'username': 'user', 'email': 'email@example.com'},
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_login_view_behavior_for_not_logged_users_user_is_None(self) -> None:
        """Tests view behavior at "/conta/entrar" for not logged users and user is None"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

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

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_login_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/conta/entrar" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGIN_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(self.LOGIN_URL, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_logout_view_behavior_for_not_logged_users(self) -> None:
        """Tests view behavior at "/conta/sair" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGOUT_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.LOGIN_URL + '?next=' + self.LOGOUT_URL)

        res: HttpResponse = self.client.get(self.LOGOUT_URL, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_logout_GET_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at GET "/conta/sair" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(self.LOGOUT_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/logout.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_logout_POST_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at POST "/conta/sair" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(self.LOGOUT_URL)

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertEqual(res.status_code, 302)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(self.LOGOUT_URL, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_activate_account_GET_view_behavior_for_not_logged_users_no_parameter(
        self,
    ) -> None:
        """Tests view behavior at GET "/conta/ativar/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_parameter'), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_activate_account_GET_view_behavior_for_not_logged_users_missing_token(
        self,
    ) -> None:
        """Tests view behavior at GET "/conta/ativar/<Any>" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_token', args=['404'])
        )

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: HttpResponse = self.client.get(
            reverse('account:activate_no_token', args=['404']), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_activate_account_GET_view_behavior_for_not_logged_users_invalid_uidb64(
        self,
    ) -> None:
        """Tests view behavior at GET "/conta/ativar/<uidb64>/<token>" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=['404', 'x' * 64])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_activate_account_GET_view_behavior_for_not_logged_users_inexistent_token(
        self,
    ) -> None:
        """Tests view behavior at GET "/conta/ativar/<uidb64>/<token>" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        user_pk: str = User.objects.first().pk
        uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, 'x' * 64])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_activate_account_GET_view_behavior_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at GET "/conta/ativar/<uidb64>/<token>" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        user_pk: str = User.objects.first().pk
        uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64, used=False
        )

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_activate_account_GET_view_behavior_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at GET "/conta/ativar/<uidb64>/<token>" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        user_pk: str = User.objects.first().pk
        uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64, used=False
        )

        res: HttpResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
