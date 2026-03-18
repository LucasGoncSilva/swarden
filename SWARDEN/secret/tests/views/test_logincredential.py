from __future__ import annotations

from typing import TYPE_CHECKING

from account.models import User
from django.test import TestCase
from django.urls import reverse

from secret.models import (
    LoginCredential,
    Service,
)
from secret.views import (
    EMPTY_POST_MSG,
    MISSING_CRITICAL_INFO,
    SLUG_ALREADY_EXISTS_MSG,
)


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class BaseLoginCredentialTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

        self.service_1: Service = Service.objects.create(name='Service 1')
        self.service_2: Service = Service.objects.create(name='Service 2')

        self.login_credential1: LoginCredential = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_1,
            name='Personal Main Account',
            slug='service-1-personal-main-account',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        )

        LoginCredential.objects.create(
            owner=self.user,
            service=self.service_2,
            name='Little Fries',
            slug='service-2-little-fries',
            third_party_login=True,
            third_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        )


class LoginCredentialCreateViewsTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/new | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:credential_create_view')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:credential_create_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/new | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:credential_create_view')
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Login Credential')

    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /secrets/credentials/new | anon user | empty form"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'), data={}
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'),
            data={},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /secrets/credentials/new | auth user | empty form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'),
            data={},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, EMPTY_POST_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Login Credential')

    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/credentials/new | anon user | existent secret slug"""

        data: dict[str, str | bool | User] = {
            'service': self.service_1.pk,
            'name': 'Personal Main Account',
            'slug': 'service-1-personal-main-account',
            'third_party_login': False,
            'third_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'), data=data
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/credentials/new | auth user | empty form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | User] = {
            'service': self.service_1.pk,
            'name': 'Personal Main Account',
            'slug': 'service-1-personal-main-account',
            'third_party_login': False,
            'third_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, SLUG_ALREADY_EXISTS_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Login Credential')

    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /secrets/credentials/new | auth user | valid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | User] = {
            'service': self.service_1.pk,
            'name': 'Another Personal Main Account',
            'slug': 'service-1-another-personal-main-account',
            'third_party_login': False,
            'third_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:credential_create_view'),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Credential/detail_view.html')


class LoginCredentialListViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/ | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:credential_list_view')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse('secret:credential_list_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:credential_list_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/ | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:credential_list_view')
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(res.context['object_list']), 2)
        self.assertEqual(res.context['model_name'], 'Login Credentials')


class LoginCredentialDetailViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/<slug:slug> | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'service-1-personal-main-account'},
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
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/<slug:slug> | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Credential/detail_view.html')
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='service-1-personal-main-account'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_detail_view',
                kwargs={'slug': 'lasagna--double-pizza'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')


class LoginCredentialUpdateViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/edit | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'service-1-personal-main-account'},
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
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/edit | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Login Credential')
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='service-1-personal-main-account'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'lasagna--double-pizza'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')

    def test_POST_authenticated_user_invalid_form(self) -> None:
        """POST /secrets/credentials/<slug:slug>/edit | auth user | invalid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | User] = {
            'owner': self.user.pk,
            'service': self.service_1.pk,
            'name': 'Personal Main Account',
            'slug': 'service-1-personal-main-account',
            'third_party_login': False,
            'third_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, MISSING_CRITICAL_INFO, status_code=422)
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Login Credential')
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='service-1-personal-main-account'
            ),
        )

    def test_POST_authenticated_user_existing_model(self) -> None:
        """POST /secrets/credentials/<slug:slug>/edit | auth user | model already exists"""  # noqa: E501

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | User] = {
            'pk': self.login_credential1.pk,
            'owner': self.user.pk,
            'service': self.service_2.pk,
            'name': 'Little Fries',
            'slug': 'service-2-little-fries',
            'third_party_login': False,
            'third_party_login_name': '-----',
            'login': 'night_monkey123@gmail.com',
            'password': 'ilovemenotyou',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, SLUG_ALREADY_EXISTS_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Login Credential')
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='service-1-personal-main-account'
            ),
        )

    def test_POST_authenticated_user_success(self) -> None:
        """POST /secrets/credentials/<slug:slug>/edit | auth user | success"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | User] = {
            'pk': self.login_credential1.pk,
            'owner': self.user.pk,
            'service': self.service_2.pk,
            'name': 'Personal Main Account',
            'slug': 'service-2-personal-main-account',
            'third_party_login': False,
            'third_party_login_name': '-----',
            'login': 'night_monkey1234@gmail.com',
            'password': 'ilovemenotyou',
            'note': 'Random note',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:credential_update_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse(
                'secret:credential_detail_view',
                args=('service-2-personal-main-account',),
            ),
        )


class LoginCredentialDeleteViewTestCase(BaseLoginCredentialTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/delete | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'service-1-personal-main-account'},
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
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/delete | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'service-1-personal-main-account'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertEqual(res.context['action'], 'Deletion')
        self.assertEqual(res.context['model'], 'Login Credential')
        self.assertEqual(
            res.context['object'],
            LoginCredential.objects.get(
                owner=User.objects.first(), slug='service-1-personal-main-account'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:credential_delete_view',
                kwargs={'slug': 'lasagna--double-pizza'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')
