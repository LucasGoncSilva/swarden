from __future__ import annotations

from typing import TYPE_CHECKING

from account.models import User
from django.test import TestCase
from django.urls import reverse


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class HomeViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='user',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /plans | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('plans:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'plans/index.html')
        self.assertContains(res, '$0')
        self.assertContains(res, '$2.99')
        self.assertContains(res, '$29.99')

    def test_GET_authenticated_user(self) -> None:
        """GET /plans | authenticated user"""

        # Confirm user login
        self.assertTrue(self.client.login(username='user', password='longpassphrase'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('plans:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'plans/index.html')
        self.assertContains(res, '$0')
        self.assertContains(res, '$2.99')
        self.assertContains(res, '$29.99')
