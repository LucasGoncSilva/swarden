from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user

from account.models import User


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

    def test_logout_view_behavior_for_logged_users(self) -> None:
        """Tests view behavior at "/conta/sair" for logged users"""

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
