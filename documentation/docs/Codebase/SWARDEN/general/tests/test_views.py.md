# File: `test_views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.general.tests`

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



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class IndexViewTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class IndexViewTestCase(TestCase):

        def setUp(self) -> None:
            User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')

        def test_GET_anonymous_user(self) -> None:
            """GET /geral/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('general:index'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('general:index'))
            res: HttpResponse = self.client.get(reverse('general:index'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /geral/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('general:index'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'general/index.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user(self) -> None:
            """POST /geral/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('general:index'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'general/index.html')
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

    GET /geral/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /geral/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('general:index'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + reverse('general:index'))
        res: HttpResponse = self.client.get(reverse('general:index'), follow=True)
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

    GET /geral/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /geral/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('general:index'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'general/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /geral/ | anonymous user

??? example "Snippet"

    ```py
    def test_POST_authenticated_user(self) -> None:
        """POST /geral/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('general:index'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'general/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
