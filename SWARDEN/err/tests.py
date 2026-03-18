from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase
from django.urls import reverse


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class Error403ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /error/403"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('err:403'))

        # Success response check
        self.assertEqual(res.status_code, 403)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context['code'], 403)
        self.assertEqual(
            res.context['message1'], 'You do not have permission to proceed.'
        )
        self.assertEqual(
            res.context['message2'],
            'Return to where you were or go to the homepage.',
        )


class Error404ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /error/404"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('err:404'))

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context['code'], 404)
        self.assertEqual(res.context['message1'], 'Page not found.')
        self.assertEqual(
            res.context['message2'],
            'Return to where you were or go to the homepage.',
        )


class Error429ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /error/429"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('err:429'))

        # Success response check
        self.assertEqual(res.status_code, 429)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context['code'], 429)
        self.assertEqual(res.context['message1'], 'Too many requests.')
        self.assertEqual(
            res.context['message2'],
            'Slow down, you do not need to be this fast here.',
        )


class Error500ViewTestCase(TestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /error/500"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('err:500'))

        # Success response check
        self.assertEqual(res.status_code, 500)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context['code'], 500)
        self.assertEqual(
            res.context['message1'],
            'There was a problem with the server.',
        )
        self.assertEqual(
            res.context['message2'],
            'Please report the issue to the website team.',
        )
