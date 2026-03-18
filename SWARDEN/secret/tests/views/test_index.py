from __future__ import annotations

from typing import TYPE_CHECKING

from account.models import User
from django.test import TestCase
from django.urls import reverse


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class SecretIndexViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/ | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('secret:index'))

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('account:login') + '?next=' + reverse('secret:index')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:index'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/ | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('secret:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
