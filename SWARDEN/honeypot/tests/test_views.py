from django.http import HttpResponse
from django.test import TestCase
from django.contrib.auth import get_user
from django.urls import reverse

from account.models import User
from honeypot.models import Attempt


class HoneypotViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='password',
            email='email@example.com',
        )

    def test_honeypot_view_behavior_with_GET_method_and_no_argument_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at GET "/admin/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:empty_redirect'), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_GET_method_and_no_argument_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at GET "/admin/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:empty_redirect'), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_no_argument_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:empty_redirect'), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_no_argument_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:empty_redirect'), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_GET_method_and_argument_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at GET "/admin/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_GET_method_and_argument_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at GET "/admin/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.get(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_argument_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_argument_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>'])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']),
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_username_in_form_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': 'username'},
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': '\' OR 1=1 --'},
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_username_in_form_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': 'username'},
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'username': '\' OR 1=1 --'},
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_password_in_form_for_not_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for not logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'password'},
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'drop table'},
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_honeypot_view_behavior_with_POST_method_and_password_in_form_for_logged_users(
        self,
    ) -> None:
        """Tests view behavior at POST "/admin/" for logged users"""

        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)

        self.assertTrue(self.client.login(username='user', password='password'))

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'password'},
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')

        res: HttpResponse = self.client.post(
            reverse('honeypot:honeypot'),
            {'password': 'drop table'},
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
