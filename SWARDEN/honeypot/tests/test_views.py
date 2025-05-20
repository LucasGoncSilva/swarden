from account.models import User
from django.contrib.auth import get_user
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from honeypot.models import Attempt


class HoneypotViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            passphrase='passphrase',
            email='user@email.com',
        )

    def test_GET_anonymous_user_no_argument(self) -> None:
        """GET /admin/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:empty_redirect'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user_no_argument(self) -> None:
        """GET /admin/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:empty_redirect'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_no_argument(self) -> None:
        """POST /admin/ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:empty_redirect'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_no_argument(self) -> None:
        """POST /admin/ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:empty_redirect'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_GET_anonymous_user_argument(self) -> None:
        """GET /admin/^(?P<path>.*)/$ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_GET_authenticated_user_argument(self) -> None:
        """GET /admin/^(?P<path>.*)/$ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_argument(self) -> None:
        """POST /admin/^(?P<path>.*)/$ | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_argument(self) -> None:
        """POST /admin/^(?P<path>.*)/$ | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_posting_username(self) -> None:
        """POST /admin/login | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': 'username'},
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': "' OR 1=1 --"},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_posting_username(self) -> None:
        """POST /admin/login | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': 'username'},
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': "' OR 1=1 --"},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_POST_anonymous_user_posting_password(self) -> None:
        """POST /admin/login | anonymous user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'password'},
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'drop table'},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_POST_authenticated_user_posting_password(self) -> None:
        """POST /admin/login | authenticated user"""

        # Anonymous user check
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        # Confirm user login
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'password'},
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'drop table'},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        # Logged user check
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
