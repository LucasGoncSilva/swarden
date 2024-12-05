
# File: `test_views.py`
Path: `SWARDEN.honeypot.tests`



---

## Imports

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```

### `#!py import get_user`

Path: `#!py django.contrib.auth`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.contrib.auth import get_user
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import TestCase`

Path: `#!py django.test`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.test import TestCase
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.urls import reverse
    ```

### `#!py import Attempt`

Path: `#!py honeypot.models`

Category: Local

??? example "SNIPPET"

    ```py
    from honeypot.models import Attempt
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class HoneypotViewsTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class HoneypotViewsTestCase(TestCase):

        def setUp(self) -> None:
            User.objects.create_user(username='user', password='password', email='user@email.com')

        def test_GET_anonymous_user_no_argument(self) -> None:
            """GET /admin/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/honeypot.html')
            res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/honeypot.html')
            self.assertEqual(Attempt.objects.all().count(), 0)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user_no_argument(self) -> None:
            """GET /admin/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            self.assertEqual(Attempt.objects.all().count(), 0)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_no_argument(self) -> None:
            """POST /admin/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_no_argument(self) -> None:
            """POST /admin/ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_argument(self) -> None:
            """GET /admin/^(?P<path>.*)/$ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/honeypot.html')
            res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/honeypot.html')
            self.assertEqual(Attempt.objects.all().count(), 0)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user_argument(self) -> None:
            """GET /admin/^(?P<path>.*)/$ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            self.assertEqual(Attempt.objects.all().count(), 0)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_argument(self) -> None:
            """POST /admin/^(?P<path>.*)/$ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_argument(self) -> None:
            """POST /admin/^(?P<path>.*)/$ | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_posting_username(self) -> None:
            """POST /admin/login | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': 'username'})
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': "' OR 1=1 --"}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_posting_username(self) -> None:
            """POST /admin/login | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': 'username'})
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': "' OR 1=1 --"}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_posting_password(self) -> None:
            """POST /admin/login | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'password'})
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'drop table'}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/loop.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user_posting_password(self) -> None:
            """POST /admin/login | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', password='password'))
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'password'})
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'drop table'}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'honeypot/authenticated.html')
            self.assertEqual(Attempt.objects.all().count(), 2)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```



---

## Functions

### `#!py def setUp`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def setUp(self) -> None:
        User.objects.create_user(username='user', password='password', email='user@email.com')
    ```

### `#!py def test_GET_anonymous_user_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user_no_argument(self) -> None:
        """GET /admin/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_no_argument(self) -> None:
        """GET /admin/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        res: HttpResponse = self.client.get(reverse('honeypot:empty_redirect'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_anonymous_user_no_argument(self) -> None:
        """POST /admin/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_no_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_authenticated_user_no_argument(self) -> None:
        """POST /admin/ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        res: HttpResponse = self.client.post(reverse('honeypot:empty_redirect'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user_argument(self) -> None:
        """GET /admin/^(?P<path>.*)/$ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/honeypot.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user_argument(self) -> None:
        """GET /admin/^(?P<path>.*)/$ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        res: HttpResponse = self.client.get(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 0)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_anonymous_user_argument(self) -> None:
        """POST /admin/^(?P<path>.*)/$ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_argument`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_authenticated_user_argument(self) -> None:
        """POST /admin/^(?P<path>.*)/$ | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        res: HttpResponse = self.client.post(reverse('honeypot:re_redirect', args=['<script>alert(1)</script>']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_posting_username`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_anonymous_user_posting_username(self) -> None:
        """POST /admin/login | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': 'username'})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': "' OR 1=1 --"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_posting_username`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_authenticated_user_posting_username(self) -> None:
        """POST /admin/login | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': 'username'})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'username': "' OR 1=1 --"}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_posting_password`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_anonymous_user_posting_password(self) -> None:
        """POST /admin/login | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'password'})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'drop table'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/loop.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_authenticated_user_posting_password`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_POST_authenticated_user_posting_password(self) -> None:
        """POST /admin/login | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', password='password'))
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'password'})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        res: HttpResponse = self.client.post(reverse('honeypot:honeypot'), {'password': 'drop table'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'honeypot/authenticated.html')
        self.assertEqual(Attempt.objects.all().count(), 2)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
