from __future__ import annotations

from typing import TYPE_CHECKING

from account.models import User
from django.test import TestCase
from django.urls import reverse

from secret.models import (
    NoteType,
    SecurityNote,
)
from secret.views import (
    EMPTY_POST_MSG,
    MISSING_CRITICAL_INFO,
    SLUG_ALREADY_EXISTS_MSG,
)


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class BaseSecurityNoteTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

        self.note_type_1: NoteType = NoteType.objects.create(name='Type 1')
        self.note_type_2: NoteType = NoteType.objects.create(name='Type 2')

        self.security_note1: SecurityNote = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            note_type=self.note_type_1,
            slug='how-to-draw-an-apple',
            content='Just draw an apple tree and erase the tree.',
        )

        SecurityNote.objects.create(
            owner=self.user,
            title='How not to draw an apple',
            note_type=self.note_type_2,
            slug='how-not-to-draw-an-apple',
            content='Just not draw an apple tree and not erase the tree.',
        )


class SecurityNoteCreateViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_create_anonymous_user(self) -> None:
        """GET /secrets/notes/new | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_create_view')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:note_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_create_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_create_authenticated_user(self) -> None:
        """GET /secrets/notes/new | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_create_view')
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Security Note')

    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /secrets/notes/new | anon user | empty form"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'), data={}
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:note_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'),
            data={},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /secrets/notes/new | auth user | empty form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'),
            data={},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, EMPTY_POST_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Security Note')

    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """GET /secrets/notes/new | anon user | existent secret slug"""

        data: dict[str, str | User] = {
            'title': 'How to draw an apple',
            'slug': 'how-to-draw-an-apple',
            'note_type': self.note_type_2.pk,
            'content': 'Just draw an apple tree and erase the tree.',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'), data=data
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:note_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/notes/new | auth user | empty form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | User] = {
            'title': 'How to draw an apple',
            'slug': 'how-to-draw-an-apple',
            'note_type': self.note_type_2.pk,
            'content': 'Just draw an apple tree and erase the tree.',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, SLUG_ALREADY_EXISTS_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Security Note')

    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /secrets/notes/new | auth user | valid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | User] = {
            'title': 'How to program with no bugs',
            'slug': 'how-to-program-with-no-bugs',
            'note_type': self.note_type_2.pk,
            'content': 'Just do not program.',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:note_create_view'),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Note/detail_view.html')


class SecurityNoteListViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_list_anonymous_user(self) -> None:
        """GET /secrets/notes/ | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_list_view')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('account:login') + '?next=' + reverse('secret:note_list_view')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_list_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_list_authenticated_user(self) -> None:
        """GET /secrets/notes/ | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_list_view')
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(res.context['object_list']), 2)
        self.assertEqual(res.context['model_name'], 'Security Notes')


class SecurityNoteDetailViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_detail_anonymous_user(self) -> None:
        """GET /secrets/notes/<slug:slug> | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
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

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_detail_authenticated_user(self) -> None:
        """GET /secrets/notes/<slug:slug> | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Note/detail_view.html')
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_detail_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')


class SecurityNoteUpdateViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_update_anonymous_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/edit | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
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

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_update_authenticated_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/edit | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Security Note')
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_update_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')

    def test_POST_authenticated_user_invalid_form(self) -> None:
        """POST /secrets/notes/<slug:slug>/edit | auth user | invalid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool] = {
            'title': 'How not to draw an apple',
            'slug': 'how-not-to-draw-an-apple',
            'note_type': self.note_type_1.pk,
            'content': 'Just draw an apple tree and erase the tree v2.',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:note_update_view',
                kwargs={'slug': 'how-to-draw-an-apple'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, MISSING_CRITICAL_INFO, status_code=422)
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Security Note')
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

    def test_POST_authenticated_user_existing_model(self) -> None:
        """POST /secrets/notes/<slug:slug>/edit | auth user | model already exists"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool] = {
            'pk': self.security_note1.pk,
            'title': 'How not to draw an apple',
            'note_type': self.note_type_1.pk,
            'slug': 'how-not-to-draw-an-apple',
            'content': 'Just draw an apple tree and erase the tree v2.',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:note_update_view',
                kwargs={'slug': 'how-to-draw-an-apple'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, SLUG_ALREADY_EXISTS_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Security Note')
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

    def test_POST_authenticated_user_success(self) -> None:
        """POST /secrets/notes/<slug:slug>/edit | auth user | success"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool] = {
            'pk': self.security_note1.pk,
            'title': 'How to draw an apple properly',
            'note_type': self.note_type_1.pk,
            'slug': 'how-to-draw-an-apple-properly',
            'content': 'Just draw an apple tree and erase the tree properly.',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:note_update_view',
                kwargs={'slug': 'how-to-draw-an-apple'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('secret:note_detail_view', args=('how-to-draw-an-apple-properly',)),
        )


class SecurityNoteDeleteViewTestCase(BaseSecurityNoteTestCase):
    def test_GET_delete_anonymous_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/delete | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
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

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_delete_authenticated_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/delete | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'})
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertEqual(res.context['action'], 'Deletion')
        self.assertEqual(res.context['model'], 'Security Note')
        self.assertEqual(
            res.context['object'],
            SecurityNote.objects.get(
                owner=User.objects.first(), slug='how-to-draw-an-apple'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:note_delete_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')
