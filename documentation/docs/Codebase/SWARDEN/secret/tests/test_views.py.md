# File: `test_views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret.tests`

No file docstring provided.

---

## Imports

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```

### `#!py import get_user`

Path: `#!py django.contrib.auth`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth import get_user
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import TestCase`

Path: `#!py django.test`

Category: trdparty

??? example "Snippet"

    ```py
    from django.test import TestCase
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: trdparty

??? example "Snippet"

    ```py
    from django.urls import reverse
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import PaymentCard`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import PaymentCard
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import SecurityNote
    ```

### `#!py import Month`

Path: `#!py secret.month.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.month.models import Month
    ```

### `#!py import EMPTY_POST_MSG`

Path: `#!py secret.views`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.views import EMPTY_POST_MSG
    ```

### `#!py import FEEDBACK_MSG`

Path: `#!py secret.views`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.views import FEEDBACK_MSG
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class SecretIndexViewTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecretIndexViewTestCase(TestCase):

        def setUp(self) -> None:
            User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')

        def test_GET_anonymous_user(self) -> None:
            """GET /secrets/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:index'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:index'))
            res: HttpResponse = self.client.get(reverse('secret:index'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /secrets/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:index'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/index.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class BaseLoginCredentialTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class BaseLoginCredentialTestCase(TestCase):

        def setUp(self) -> None:
            self.user: User = User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
            LoginCredential.objects.create(owner=self.user, service='google--', name='Personal Main Account', slug='google--personal-main-account', third_party_login=False, third_party_login_name='-----', login='night_monkey123@gmail.com', password='ilovemenotyou')
            LoginCredential.objects.create(owner=self.user, service='steam--', name='Little Fries', slug='steam--little-fries', third_party_login=True, third_party_login_name='Personal Main Account', login='-----', password='-----')
    ```

### `#!py class LoginCredentialCreateViewsTestCase`

Parents: `BaseLoginCredentialTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginCredentialCreateViewsTestCase(BaseLoginCredentialTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /secrets/credentials/new | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:credential_create_view'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_create_view'))
            res: HttpResponse = self.client.get(reverse('secret:credential_create_view'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /secrets/credentials/new | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:credential_create_view'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Credencial')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_form(self) -> None:
            """POST /secrets/credentials/new | anonymous user | empty form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), {})
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_create_view'))
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), {}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_empty_form(self) -> None:
            """POST /secrets/credentials/new | authenticated user | empty form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), {}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Credencial')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
            """POST /secrets/credentials/new | anonymous user | existent secret slug"""
            cred_data: dict = {'owner': self.user, 'service': 'google--', 'name': 'Personal Main Account', 'slug': 'google--personal-main-account', 'third_party_login': False, 'third_party_login_name': '-----', 'login': 'night_monkey123@gmail.com', 'password': 'ilovemenotyou'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data)
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_create_view'))
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
            """POST /secrets/credentials/new | authenticated user | empty form"""
            cred_data: dict = {'owner': self.user, 'service': 'google--', 'name': 'Personal Main Account', 'slug': 'google--personal-main-account', 'third_party_login': False, 'third_party_login_name': '-----', 'login': 'night_monkey123@gmail.com', 'password': 'ilovemenotyou'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Credencial')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_valid_form(self) -> None:
            """POST /secrets/credentials/new | authenticated user | valid form"""
            cred_data: dict = {'owner': self.user, 'service': 'google--', 'name': 'Another Personal Main Account', 'slug': 'google--another-personal-main-account', 'third_party_login': False, 'third_party_login_name': '-----', 'login': 'night_monkey123@gmail.com', 'password': 'ilovemenotyou'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Credencial')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class LoginCredentialListViewTestCase`

Parents: `BaseLoginCredentialTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginCredentialListViewTestCase(BaseLoginCredentialTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /secrets/credentials/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:credential_list_view'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_list_view'))
            res: HttpResponse = self.client.get(reverse('secret:credential_list_view'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /secrets/credentials/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:credential_list_view'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertIn('object_list', res.context.keys())
            self.assertEqual(len(res.context['object_list']), 2)
            self.assertIn('model_name', res.context.keys())
            self.assertEqual(res.context['model_name'], 'Credenciais')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class LoginCredentialDetailViewTestCase`

Parents: `BaseLoginCredentialTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginCredentialDetailViewTestCase(BaseLoginCredentialTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /secrets/credentials/<slug:slug> | anonymous user"""
            res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}))
            res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /secrets/credentials/<slug:slug> | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/Credential/detail_view.html')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], LoginCredential.objects.get(owner=User.objects.first(), slug='google--personal-main-account'))
            res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class LoginCredentialUpdateViewTestCase`

Parents: `BaseLoginCredentialTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginCredentialUpdateViewTestCase(BaseLoginCredentialTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /secrets/credentials/<slug:slug>/edit | anonymous user"""
            res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}))
            res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /secrets/credentials/<slug:slug>/edit | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Edição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Credencial')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], LoginCredential.objects.get(owner=User.objects.first(), slug='google--personal-main-account'))
            res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class LoginCredentialDeleteViewTestCase`

Parents: `BaseLoginCredentialTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginCredentialDeleteViewTestCase(BaseLoginCredentialTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /secrets/credentials/<slug:slug>/delete | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}))
            res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /secrets/credentials/<slug:slug>/delete | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/delete_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Exclusão')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Credencial')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], LoginCredential.objects.get(owner=User.objects.first(), slug='google--personal-main-account'))
            res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class BaseCardTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class BaseCardTestCase(TestCase):

        def setUp(self) -> None:
            self.user: User = User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
            PaymentCard.objects.create(owner=self.user, name='Personal Main Card', card_type='deb', number='4002892240028922', expiration=Month(2028, 11), cvv='113', bank='nubank--', brand='mastercard--', slug='nubank--personal-main-card', owners_name='TEST USER')
    ```

### `#!py class CardCreateViewsTestCase`

Parents: `BaseCardTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class CardCreateViewsTestCase(BaseCardTestCase):

        def test_GET_create_anonymous_user(self) -> None:
            """GET /secrets/payment-cards/new | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:card_create_view'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_create_view'))
            res: HttpResponse = self.client.get(reverse('secret:card_create_view'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_create_authenticated_user(self) -> None:
            """GET /secrets/payment-cards/new | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:card_create_view'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Cartão')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_form(self) -> None:
            """POST /secrets/payment-cards/new | anonymous user | empty form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {})
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_create_view'))
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_empty_form(self) -> None:
            """POST /secrets/payment-cards/new | authenticated user | empty form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Cartão')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
            """GET /secrets/payment-cards/new | anonymous user | existent secret slug"""
            card_data: dict = {'owner': self.user, 'name': 'Personal Main Card', 'card_type': 'deb', 'number': '4002892240028922', 'expiration_0': '11', 'expiration_1': '2028', 'cvv': '113', 'bank': 'nubank--', 'brand': 'mastercard--', 'slug': 'nubank--personal-main-card', 'owners_name': 'TEST USER'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data)
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_create_view'))
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
            """POST /secrets/payment-cards/new | authenticated user | empty form"""
            card_data: dict = {'owner': self.user, 'name': 'Personal Main Card', 'card_type': 'deb', 'number': '4002892240028922', 'expiration_0': '11', 'expiration_1': '2028', 'cvv': '113', 'bank': 'nubank--', 'brand': 'mastercard--', 'slug': 'nubank--personal-main-card', 'owners_name': 'TEST USER'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Cartão')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_valid_form(self) -> None:
            """POST /secrets/payment-cards/new | authenticated user | valid form"""
            card_data: dict = {'owner': self.user, 'name': 'Another Personal Main Card', 'card_type': 'deb', 'number': '4002892240028922', 'expiration_0': '11', 'expiration_1': '2028', 'cvv': '113', 'bank': 'nubank--', 'brand': 'mastercard--', 'slug': 'nubank--another-personal-main-card', 'owners_name': 'TEST USER'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Cartão')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class CardListViewTestCase`

Parents: `BaseCardTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class CardListViewTestCase(BaseCardTestCase):

        def test_GET_list_anonymous_user(self) -> None:
            """GET /secrets/payment-cards/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:card_list_view'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_list_view'))
            res: HttpResponse = self.client.get(reverse('secret:card_list_view'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_list_authenticated_user(self) -> None:
            """GET /secrets/payment-cards/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:card_list_view'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertIn('object_list', res.context.keys())
            self.assertEqual(len(res.context['object_list']), 1)
            self.assertIn('model_name', res.context.keys())
            self.assertEqual(res.context['model_name'], 'Cartões')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class CardDetailViewTestCase`

Parents: `BaseCardTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class CardDetailViewTestCase(BaseCardTestCase):

        def test_GET_detail_anonymous_user(self) -> None:
            """GET /secrets/payment-cards/<slug:slug> | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}))
            res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_detail_authenticated_user(self) -> None:
            """GET /secrets/payment-cards/<slug:slug> | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/Card/detail_view.html')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], PaymentCard.objects.get(owner=User.objects.first(), slug='nubank--personal-main-card'))
            res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class CardUpdateViewTestCase`

Parents: `BaseCardTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class CardUpdateViewTestCase(BaseCardTestCase):

        def test_GET_update_anonymous_user(self) -> None:
            """GET /secrets/payment-cards/<slug:slug>/edit | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}))
            res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_update_authenticated_user(self) -> None:
            """GET /secrets/payment-cards/<slug:slug>/edit | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Edição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Cartão')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], PaymentCard.objects.get(owner=User.objects.first(), slug='nubank--personal-main-card'))
            res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class CardDeleteViewTestCase`

Parents: `BaseCardTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class CardDeleteViewTestCase(BaseCardTestCase):

        def test_GET_delete_anonymous_user(self) -> None:
            """GET /secrets/payment-cards/<slug:slug>/delete | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}))
            res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_delete_authenticated_user(self) -> None:
            """GET /secrets/payment-cards/<slug:slug>/delete | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/delete_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Exclusão')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Cartão')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], PaymentCard.objects.get(owner=User.objects.first(), slug='nubank--personal-main-card'))
            res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class BaseSecurityNoteTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class BaseSecurityNoteTestCase(TestCase):

        def setUp(self) -> None:
            self.user: User = User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
            SecurityNote.objects.create(owner=self.user, title='How to draw an apple', slug='how-to-draw-an-apple', content='Just draw an apple tree and erase the tree.')
    ```

### `#!py class SecurityNoteCreateViewTestCase`

Parents: `BaseSecurityNoteTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNoteCreateViewTestCase(BaseSecurityNoteTestCase):

        def test_GET_create_anonymous_user(self) -> None:
            """GET /secrets/notes/new | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('secret:note_create_view'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_create_view'))
            res: HttpResponse = self.client.get(reverse('secret:note_create_view'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_create_authenticated_user(self) -> None:
            """GET /secrets/notes/new | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:note_create_view'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Anotação')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_form(self) -> None:
            """POST /secrets/notes/new | anonymous user | empty form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {})
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_create_view'))
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_empty_form(self) -> None:
            """POST /secrets/notes/new | authenticated user | empty form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Anotação')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
            """GET /secrets/notes/new | anonymous user | existent secret slug"""
            note_data: dict = {'owner': self.user, 'title': 'How to draw an apple', 'slug': 'how-to-draw-an-apple', 'content': 'Just draw an apple tree and erase the tree.'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data)
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_create_view'))
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
            """POST /secrets/notes/new | authenticated user | empty form"""
            note_data: dict = {'owner': self.user, 'title': 'How to draw an apple', 'slug': 'how-to-draw-an-apple', 'content': 'Just draw an apple tree and erase the tree.'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Anotação')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_valid_form(self) -> None:
            """POST /secrets/notes/new | authenticated user | valid form"""
            note_data: dict = {'owner': self.user, 'title': 'How not to draw an apple', 'slug': 'how-not-to-draw-an-apple', 'content': 'Just not draw an apple tree and erase the tree.'}
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Adição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Anotação')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class SecurityNoteListViewTestCase`

Parents: `BaseSecurityNoteTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNoteListViewTestCase(BaseSecurityNoteTestCase):

        def test_GET_list_anonymous_user(self) -> None:
            """GET /secrets/notes/ | anonymous user"""
            res: HttpResponse = self.client.get(reverse('secret:note_list_view'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_list_view'))
            res: HttpResponse = self.client.get(reverse('secret:note_list_view'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_list_authenticated_user(self) -> None:
            """GET /secrets/notes/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:note_list_view'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/list_view.html')
            self.assertIn('object_list', res.context.keys())
            self.assertEqual(len(res.context['object_list']), 1)
            self.assertIn('model_name', res.context.keys())
            self.assertEqual(res.context['model_name'], 'Anotações')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class SecurityNoteDetailViewTestCase`

Parents: `BaseSecurityNoteTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNoteDetailViewTestCase(BaseSecurityNoteTestCase):

        def test_GET_detail_anonymous_user(self) -> None:
            """GET /secrets/notes/<slug:slug> | anonymous user"""
            res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_detail_authenticated_user(self) -> None:
            """GET /secrets/notes/<slug:slug> | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/Note/detail_view.html')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], SecurityNote.objects.get(owner=User.objects.first(), slug='how-to-draw-an-apple'))
            res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class SecurityNoteUpdateViewTestCase`

Parents: `BaseSecurityNoteTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNoteUpdateViewTestCase(BaseSecurityNoteTestCase):

        def test_GET_update_anonymous_user(self) -> None:
            """GET /secrets/notes/<slug:slug>/edit | anonymous user"""
            res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_update_authenticated_user(self) -> None:
            """GET /secrets/notes/<slug:slug>/edit | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/create_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Edição')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Anotação')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], SecurityNote.objects.get(owner=User.objects.first(), slug='how-to-draw-an-apple'))
            res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class SecurityNoteDeleteViewTestCase`

Parents: `BaseSecurityNoteTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNoteDeleteViewTestCase(BaseSecurityNoteTestCase):

        def test_GET_delete_anonymous_user(self) -> None:
            """GET /secrets/notes/<slug:slug>/delete | anonymous user"""
            res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_delete_authenticated_user(self) -> None:
            """GET /secrets/notes/<slug:slug>/delete | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'secret/delete_view.html')
            self.assertIn('action', res.context.keys())
            self.assertEqual(res.context['action'], 'Exclusão')
            self.assertIn('model', res.context.keys())
            self.assertEqual(res.context['model'], 'Anotação')
            self.assertIn('object', res.context.keys())
            self.assertEqual(res.context['object'], SecurityNote.objects.get(owner=User.objects.first(), slug='how-to-draw-an-apple'))
            res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'lasagna--double-pizza'}))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```



---

## Functions

### `#!py def setUp`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def setUp(self) -> None:
        User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:index'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:index'))
        res: HttpResponse = self.client.get(reverse('secret:index'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/ | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:index'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def setUp`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
        LoginCredential.objects.create(owner=self.user, service='google--', name='Personal Main Account', slug='google--personal-main-account', third_party_login=False, third_party_login_name='-----', login='night_monkey123@gmail.com', password='ilovemenotyou')
        LoginCredential.objects.create(owner=self.user, service='steam--', name='Little Fries', slug='steam--little-fries', third_party_login=True, third_party_login_name='Personal Main Account', login='-----', password='-----')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/new | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/new | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:credential_create_view'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_create_view'))
        res: HttpResponse = self.client.get(reverse('secret:credential_create_view'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/new | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/new | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:credential_create_view'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/credentials/new | anonymous user | empty form

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /secrets/credentials/new | anonymous user | empty form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), {})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_create_view'))
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), {}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_empty_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/credentials/new | authenticated user | empty form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /secrets/credentials/new | authenticated user | empty form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), {}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_form_existing_secret`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/credentials/new | anonymous user | existent secret slug

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/credentials/new | anonymous user | existent secret slug"""
        cred_data: dict = {'owner': self.user, 'service': 'google--', 'name': 'Personal Main Account', 'slug': 'google--personal-main-account', 'third_party_login': False, 'third_party_login_name': '-----', 'login': 'night_monkey123@gmail.com', 'password': 'ilovemenotyou'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_create_view'))
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_empty_form_existing_secret`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/credentials/new | authenticated user | empty form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/credentials/new | authenticated user | empty form"""
        cred_data: dict = {'owner': self.user, 'service': 'google--', 'name': 'Personal Main Account', 'slug': 'google--personal-main-account', 'third_party_login': False, 'third_party_login_name': '-----', 'login': 'night_monkey123@gmail.com', 'password': 'ilovemenotyou'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_valid_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/credentials/new | authenticated user | valid form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /secrets/credentials/new | authenticated user | valid form"""
        cred_data: dict = {'owner': self.user, 'service': 'google--', 'name': 'Another Personal Main Account', 'slug': 'google--another-personal-main-account', 'third_party_login': False, 'third_party_login_name': '-----', 'login': 'night_monkey123@gmail.com', 'password': 'ilovemenotyou'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:credential_create_view'), cred_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:credential_list_view'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_list_view'))
        res: HttpResponse = self.client.get(reverse('secret:credential_list_view'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/ | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:credential_list_view'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertIn('object_list', res.context.keys())
        self.assertEqual(len(res.context['object_list']), 2)
        self.assertIn('model_name', res.context.keys())
        self.assertEqual(res.context['model_name'], 'Credenciais')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/<slug:slug> | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/<slug:slug> | anonymous user"""
        res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}))
        res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/<slug:slug> | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/<slug:slug> | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'google--personal-main-account'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Credential/detail_view.html')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], LoginCredential.objects.get(owner=User.objects.first(), slug='google--personal-main-account'))
        res: HttpResponse = self.client.get(reverse('secret:credential_detail_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/<slug:slug>/edit | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/edit | anonymous user"""
        res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}))
        res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/<slug:slug>/edit | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/edit | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'google--personal-main-account'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Edição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], LoginCredential.objects.get(owner=User.objects.first(), slug='google--personal-main-account'))
        res: HttpResponse = self.client.get(reverse('secret:credential_update_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/<slug:slug>/delete | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/delete | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}))
        res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/credentials/<slug:slug>/delete | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /secrets/credentials/<slug:slug>/delete | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'google--personal-main-account'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Exclusão')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Credencial')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], LoginCredential.objects.get(owner=User.objects.first(), slug='google--personal-main-account'))
        res: HttpResponse = self.client.get(reverse('secret:credential_delete_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def setUp`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
        PaymentCard.objects.create(owner=self.user, name='Personal Main Card', card_type='deb', number='4002892240028922', expiration=Month(2028, 11), cvv='113', bank='nubank--', brand='mastercard--', slug='nubank--personal-main-card', owners_name='TEST USER')
    ```

### `#!py def test_GET_create_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/new | anonymous user

??? example "Snippet"

    ```py
    def test_GET_create_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/new | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:card_create_view'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_create_view'))
        res: HttpResponse = self.client.get(reverse('secret:card_create_view'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_create_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/new | authenticated user

??? example "Snippet"

    ```py
    def test_GET_create_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/new | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:card_create_view'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/payment-cards/new | anonymous user | empty form

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /secrets/payment-cards/new | anonymous user | empty form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_create_view'))
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_empty_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/payment-cards/new | authenticated user | empty form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /secrets/payment-cards/new | authenticated user | empty form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), {}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_form_existing_secret`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/new | anonymous user | existent secret slug

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """GET /secrets/payment-cards/new | anonymous user | existent secret slug"""
        card_data: dict = {'owner': self.user, 'name': 'Personal Main Card', 'card_type': 'deb', 'number': '4002892240028922', 'expiration_0': '11', 'expiration_1': '2028', 'cvv': '113', 'bank': 'nubank--', 'brand': 'mastercard--', 'slug': 'nubank--personal-main-card', 'owners_name': 'TEST USER'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_create_view'))
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_empty_form_existing_secret`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/payment-cards/new | authenticated user | empty form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/payment-cards/new | authenticated user | empty form"""
        card_data: dict = {'owner': self.user, 'name': 'Personal Main Card', 'card_type': 'deb', 'number': '4002892240028922', 'expiration_0': '11', 'expiration_1': '2028', 'cvv': '113', 'bank': 'nubank--', 'brand': 'mastercard--', 'slug': 'nubank--personal-main-card', 'owners_name': 'TEST USER'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_valid_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/payment-cards/new | authenticated user | valid form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /secrets/payment-cards/new | authenticated user | valid form"""
        card_data: dict = {'owner': self.user, 'name': 'Another Personal Main Card', 'card_type': 'deb', 'number': '4002892240028922', 'expiration_0': '11', 'expiration_1': '2028', 'cvv': '113', 'bank': 'nubank--', 'brand': 'mastercard--', 'slug': 'nubank--another-personal-main-card', 'owners_name': 'TEST USER'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:card_create_view'), card_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_list_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_list_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:card_list_view'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_list_view'))
        res: HttpResponse = self.client.get(reverse('secret:card_list_view'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_list_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/ | authenticated user

??? example "Snippet"

    ```py
    def test_GET_list_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:card_list_view'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertIn('object_list', res.context.keys())
        self.assertEqual(len(res.context['object_list']), 1)
        self.assertIn('model_name', res.context.keys())
        self.assertEqual(res.context['model_name'], 'Cartões')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_detail_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/<slug:slug> | anonymous user

??? example "Snippet"

    ```py
    def test_GET_detail_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug> | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}))
        res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_detail_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/<slug:slug> | authenticated user

??? example "Snippet"

    ```py
    def test_GET_detail_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug> | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'nubank--personal-main-card'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Card/detail_view.html')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], PaymentCard.objects.get(owner=User.objects.first(), slug='nubank--personal-main-card'))
        res: HttpResponse = self.client.get(reverse('secret:card_detail_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_update_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/<slug:slug>/edit | anonymous user

??? example "Snippet"

    ```py
    def test_GET_update_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/edit | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}))
        res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_update_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/<slug:slug>/edit | authenticated user

??? example "Snippet"

    ```py
    def test_GET_update_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/edit | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'nubank--personal-main-card'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Edição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], PaymentCard.objects.get(owner=User.objects.first(), slug='nubank--personal-main-card'))
        res: HttpResponse = self.client.get(reverse('secret:card_update_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_delete_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/<slug:slug>/delete | anonymous user

??? example "Snippet"

    ```py
    def test_GET_delete_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/delete | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}))
        res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_delete_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/payment-cards/<slug:slug>/delete | authenticated user

??? example "Snippet"

    ```py
    def test_GET_delete_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/delete | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'nubank--personal-main-card'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Exclusão')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Cartão')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], PaymentCard.objects.get(owner=User.objects.first(), slug='nubank--personal-main-card'))
        res: HttpResponse = self.client.get(reverse('secret:card_delete_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def setUp`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
        SecurityNote.objects.create(owner=self.user, title='How to draw an apple', slug='how-to-draw-an-apple', content='Just draw an apple tree and erase the tree.')
    ```

### `#!py def test_GET_create_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/new | anonymous user

??? example "Snippet"

    ```py
    def test_GET_create_anonymous_user(self) -> None:
        """GET /secrets/notes/new | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('secret:note_create_view'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_create_view'))
        res: HttpResponse = self.client.get(reverse('secret:note_create_view'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_create_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/new | authenticated user

??? example "Snippet"

    ```py
    def test_GET_create_authenticated_user(self) -> None:
        """GET /secrets/notes/new | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:note_create_view'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/notes/new | anonymous user | empty form

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /secrets/notes/new | anonymous user | empty form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_create_view'))
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_empty_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/notes/new | authenticated user | empty form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /secrets/notes/new | authenticated user | empty form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), {}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(EMPTY_POST_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_form_existing_secret`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/new | anonymous user | existent secret slug

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """GET /secrets/notes/new | anonymous user | existent secret slug"""
        note_data: dict = {'owner': self.user, 'title': 'How to draw an apple', 'slug': 'how-to-draw-an-apple', 'content': 'Just draw an apple tree and erase the tree.'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_create_view'))
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_empty_form_existing_secret`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/notes/new | authenticated user | empty form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/notes/new | authenticated user | empty form"""
        note_data: dict = {'owner': self.user, 'title': 'How to draw an apple', 'slug': 'how-to-draw-an-apple', 'content': 'Just draw an apple tree and erase the tree.'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn(FEEDBACK_MSG, res.content.decode('utf-8'))
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_valid_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /secrets/notes/new | authenticated user | valid form

??? example "Snippet"

    ```py
    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /secrets/notes/new | authenticated user | valid form"""
        note_data: dict = {'owner': self.user, 'title': 'How not to draw an apple', 'slug': 'how-not-to-draw-an-apple', 'content': 'Just not draw an apple tree and erase the tree.'}
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(reverse('secret:note_create_view'), note_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Adição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_list_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_list_anonymous_user(self) -> None:
        """GET /secrets/notes/ | anonymous user"""
        res: HttpResponse = self.client.get(reverse('secret:note_list_view'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_list_view'))
        res: HttpResponse = self.client.get(reverse('secret:note_list_view'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_list_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/ | authenticated user

??? example "Snippet"

    ```py
    def test_GET_list_authenticated_user(self) -> None:
        """GET /secrets/notes/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:note_list_view'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertIn('object_list', res.context.keys())
        self.assertEqual(len(res.context['object_list']), 1)
        self.assertIn('model_name', res.context.keys())
        self.assertEqual(res.context['model_name'], 'Anotações')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_detail_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/<slug:slug> | anonymous user

??? example "Snippet"

    ```py
    def test_GET_detail_anonymous_user(self) -> None:
        """GET /secrets/notes/<slug:slug> | anonymous user"""
        res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_detail_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/<slug:slug> | authenticated user

??? example "Snippet"

    ```py
    def test_GET_detail_authenticated_user(self) -> None:
        """GET /secrets/notes/<slug:slug> | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Note/detail_view.html')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], SecurityNote.objects.get(owner=User.objects.first(), slug='how-to-draw-an-apple'))
        res: HttpResponse = self.client.get(reverse('secret:note_detail_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_update_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/<slug:slug>/edit | anonymous user

??? example "Snippet"

    ```py
    def test_GET_update_anonymous_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/edit | anonymous user"""
        res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_update_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/<slug:slug>/edit | authenticated user

??? example "Snippet"

    ```py
    def test_GET_update_authenticated_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/edit | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Edição')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], SecurityNote.objects.get(owner=User.objects.first(), slug='how-to-draw-an-apple'))
        res: HttpResponse = self.client.get(reverse('secret:note_update_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_delete_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/<slug:slug>/delete | anonymous user

??? example "Snippet"

    ```py
    def test_GET_delete_anonymous_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/delete | anonymous user"""
        res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_delete_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /secrets/notes/<slug:slug>/delete | authenticated user

??? example "Snippet"

    ```py
    def test_GET_delete_authenticated_user(self) -> None:
        """GET /secrets/notes/<slug:slug>/delete | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'how-to-draw-an-apple'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertIn('action', res.context.keys())
        self.assertEqual(res.context['action'], 'Exclusão')
        self.assertIn('model', res.context.keys())
        self.assertEqual(res.context['model'], 'Anotação')
        self.assertIn('object', res.context.keys())
        self.assertEqual(res.context['object'], SecurityNote.objects.get(owner=User.objects.first(), slug='how-to-draw-an-apple'))
        res: HttpResponse = self.client.get(reverse('secret:note_delete_view', kwargs={'slug': 'lasagna--double-pizza'}))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
