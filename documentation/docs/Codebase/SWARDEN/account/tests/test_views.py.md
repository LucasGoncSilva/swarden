# File: `test_views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account.tests`

No file docstring provided.

---

## Imports

### `#!py import cast`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import cast
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

### `#!py import force_bytes`

Path: `#!py django.utils.encoding`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.encoding import force_bytes
    ```

### `#!py import urlsafe_base64_encode`

Path: `#!py django.utils.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.utils.http import urlsafe_base64_encode
    ```

### `#!py import ActivationAccountToken`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import ActivationAccountToken
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class BaseAccountTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class BaseAccountTestCase(TestCase):

        def setUp(self) -> None:
            User.objects.create_user(username='user', passphrase='passphrase', email='user@email.com')
            self.REGISTER_URL: str = reverse('account:register')
            self.LOGIN_URL: str = reverse('account:login')
            self.LOGOUT_URL: str = reverse('account:logout')
    ```

### `#!py class RegisterViewTestCase`

Parents: `BaseAccountTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class RegisterViewTestCase(BaseAccountTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /account/register | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.REGISTER_URL)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/register.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_invalid_form(self) -> None:
            """POST /account/register | anonymous user | invalid form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(self.REGISTER_URL, {'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'})
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/register.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_different_passphrases(self) -> None:
            """POST /account/register | anonymous user | different passphrases"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            post_data: dict[str, str] = {'username': 'username', 'first_name': 'first', 'last_name': 'last', 'email': 'another@example.com', 'passphrase': '12345678', 'passphrase2': '11223344', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
            res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/register.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_existing_register(self) -> None:
            """POST /account/register | anonymous user | register already exists"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            post_data: dict[str, str] = {'username': 'user', 'first_name': 'first', 'last_name': 'last', 'email': 'email@example.com', 'passphrase': 'passphrase', 'passphrase2': 'passphrase', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
            res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/register.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_empty_names(self) -> None:
            """POST /account/register | anonymous user | empty first_name and/or last_name"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            post_data: dict[str, str | None] = {'username': 'username', 'first_name': '', 'last_name': 'last', 'email': 'email@example.com', 'passphrase': 'passphrase', 'passphrase2': 'passphrase', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
            res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/register.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_POST_anonymous_user_valid_form(self) -> None:
            """POST /account/register | anonymous user | valid form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            post_data: dict[str, str] = {'username': 'username', 'first_name': 'first', 'last_name': 'last', 'email': 'another@example.com', 'passphrase': 'passphrase', 'passphrase2': 'passphrase', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
            res: HttpResponse = self.client.post(self.REGISTER_URL, post_data, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /account/register | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.REGISTER_URL)
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('home:index'))
            res: HttpResponse = self.client.get(self.REGISTER_URL, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
    ```

### `#!py class ActivateAccountViewTestCase`

Parents: `BaseAccountTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class ActivateAccountViewTestCase(BaseAccountTestCase):

        def test_GET_anonymous_user_no_parameter(self) -> None:
            """GET /account/activate/ | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('home:index'))
            res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/landing.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_missing_token(self) -> None:
            """GET /account/activate/<Any> | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('account:activate_no_token', args=['404']))
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('home:index'))
            res: HttpResponse = self.client.get(reverse('account:activate_no_token', args=['404']), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/landing.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_invalid_uidb64(self) -> None:
            """GET /account/activate/<uidb64>/<token> | anonymous user | invalid uidb64"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('account:activate', args=['404', 'x' * 64]))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_inexistent_token(self) -> None:
            """GET /account/activate/<uidb64>/<token> | anonymous user | inexistent token"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            user: User = cast(User, User.objects.first())
            user_pk: str = user.pk
            uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))
            res: HttpResponse = self.client.get(reverse('account:activate', args=[uidb64_pk, 'x' * 64]))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user(self) -> None:
            """GET /account/activate/<uidb64>/<token> | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            user: User = cast(User, User.objects.first())
            uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token: ActivationAccountToken = ActivationAccountToken.objects.create(value='x' * 64, user=user, used=False)
            res: HttpResponse = self.client.get(reverse('account:activate', args=[uidb64_pk, token.value]), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /account/activate/<uidb64>/<token> | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            user: User = cast(User, User.objects.first())
            uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token: ActivationAccountToken = ActivationAccountToken.objects.create(value='x' * 64, user=user, used=False)
            res: HttpResponse = self.client.get(reverse('account:activate', args=[uidb64_pk, token.value]), follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py class LoginViewTestCase`

Parents: `BaseAccountTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LoginViewTestCase(BaseAccountTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /account/login | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.LOGIN_URL)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            res: HttpResponse = self.client.post(self.LOGIN_URL, {'username': 'user', 'passphrase': 'passphrase', 'email': 'email@example.com'}, follow=True)
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_invalid_form(self) -> None:
            """GET /account/login | anonymous user | invalid form"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.LOGIN_URL)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            res: HttpResponse = self.client.post(self.LOGIN_URL, {'username': 'user', 'email': 'email@example.com'}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_anonymous_user_user_is_None(self) -> None:
            """GET /account/login | anonymous user | user is None"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.LOGIN_URL)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            res: HttpResponse = self.client.post(self.LOGIN_URL, {'username': 'fake_user', 'passphrase': 'passphrase', 'email': 'email@example.com'}, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /account/login | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.LOGIN_URL)
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, reverse('home:index'))
            res: HttpResponse = self.client.get(self.LOGIN_URL, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
    ```

### `#!py class LogoutViewTestCase`

Parents: `BaseAccountTestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LogoutViewTestCase(BaseAccountTestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /account/logout | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.LOGOUT_URL)
            self.assertEqual(res.status_code, 302)
            self.assertRedirects(res, self.LOGIN_URL + '?next=' + self.LOGOUT_URL)
            res: HttpResponse = self.client.get(self.LOGOUT_URL, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self) -> None:
            """GET /account/logout | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(self.LOGOUT_URL)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/logout.html')
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)

        def test_POST_authenticated_user(self) -> None:
            """POST /account/logout | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            self.assertFalse(get_user(self.client).is_anonymous)
            self.assertTrue(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.post(self.LOGOUT_URL)
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.assertEqual(res.status_code, 302)
            self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
            res: HttpResponse = self.client.post(self.LOGOUT_URL, follow=True)
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'account/login.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
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
        self.REGISTER_URL: str = reverse('account:register')
        self.LOGIN_URL: str = reverse('account:login')
        self.LOGOUT_URL: str = reverse('account:logout')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/register | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /account/register | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.REGISTER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_invalid_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /account/register | anonymous user | invalid form

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /account/register | anonymous user | invalid form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(self.REGISTER_URL, {'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_different_passphrases`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /account/register | anonymous user | different passphrases

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_different_passphrases(self) -> None:
        """POST /account/register | anonymous user | different passphrases"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        post_data: dict[str, str] = {'username': 'username', 'first_name': 'first', 'last_name': 'last', 'email': 'another@example.com', 'passphrase': '12345678', 'passphrase2': '11223344', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_existing_register`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /account/register | anonymous user | register already exists

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_existing_register(self) -> None:
        """POST /account/register | anonymous user | register already exists"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        post_data: dict[str, str] = {'username': 'user', 'first_name': 'first', 'last_name': 'last', 'email': 'email@example.com', 'passphrase': 'passphrase', 'passphrase2': 'passphrase', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_empty_names`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /account/register | anonymous user | empty first_name and/or last_name

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_empty_names(self) -> None:
        """POST /account/register | anonymous user | empty first_name and/or last_name"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        post_data: dict[str, str | None] = {'username': 'username', 'first_name': '', 'last_name': 'last', 'email': 'email@example.com', 'passphrase': 'passphrase', 'passphrase2': 'passphrase', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_POST_anonymous_user_valid_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    POST /account/register | anonymous user | valid form

??? example "Snippet"

    ```py
    def test_POST_anonymous_user_valid_form(self) -> None:
        """POST /account/register | anonymous user | valid form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        post_data: dict[str, str] = {'username': 'username', 'first_name': 'first', 'last_name': 'last', 'email': 'another@example.com', 'passphrase': 'passphrase', 'passphrase2': 'passphrase', 'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'}
        res: HttpResponse = self.client.post(self.REGISTER_URL, post_data, follow=True)
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

    GET /account/register | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /account/register | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.REGISTER_URL)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))
        res: HttpResponse = self.client.get(self.REGISTER_URL, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
    ```

### `#!py def test_GET_anonymous_user_no_parameter`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/activate/ | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user_no_parameter(self) -> None:
        """GET /account/activate/ | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))
        res: HttpResponse = self.client.get(reverse('account:activate_no_parameter'), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_missing_token`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/activate/<Any> | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user_missing_token(self) -> None:
        """GET /account/activate/<Any> | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('account:activate_no_token', args=['404']))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))
        res: HttpResponse = self.client.get(reverse('account:activate_no_token', args=['404']), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_invalid_uidb64`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/activate/<uidb64>/<token> | anonymous user | invalid uidb64

??? example "Snippet"

    ```py
    def test_GET_anonymous_user_invalid_uidb64(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user | invalid uidb64"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('account:activate', args=['404', 'x' * 64]))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_inexistent_token`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/activate/<uidb64>/<token> | anonymous user | inexistent token

??? example "Snippet"

    ```py
    def test_GET_anonymous_user_inexistent_token(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user | inexistent token"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        user: User = cast(User, User.objects.first())
        user_pk: str = user.pk
        uidb64_pk = urlsafe_base64_encode(force_bytes(user_pk))
        res: HttpResponse = self.client.get(reverse('account:activate', args=[uidb64_pk, 'x' * 64]))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/activate/<uidb64>/<token> | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        user: User = cast(User, User.objects.first())
        uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token: ActivationAccountToken = ActivationAccountToken.objects.create(value='x' * 64, user=user, used=False)
        res: HttpResponse = self.client.get(reverse('account:activate', args=[uidb64_pk, token.value]), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/activate/<uidb64>/<token> | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /account/activate/<uidb64>/<token> | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        user: User = cast(User, User.objects.first())
        uidb64_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token: ActivationAccountToken = ActivationAccountToken.objects.create(value='x' * 64, user=user, used=False)
        res: HttpResponse = self.client.get(reverse('account:activate', args=[uidb64_pk, token.value]), follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
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

    GET /account/login | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /account/login | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.LOGIN_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        res: HttpResponse = self.client.post(self.LOGIN_URL, {'username': 'user', 'passphrase': 'passphrase', 'email': 'email@example.com'}, follow=True)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_invalid_form`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/login | anonymous user | invalid form

??? example "Snippet"

    ```py
    def test_GET_anonymous_user_invalid_form(self) -> None:
        """GET /account/login | anonymous user | invalid form"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.LOGIN_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        res: HttpResponse = self.client.post(self.LOGIN_URL, {'username': 'user', 'email': 'email@example.com'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_anonymous_user_user_is_None`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/login | anonymous user | user is None

??? example "Snippet"

    ```py
    def test_GET_anonymous_user_user_is_None(self) -> None:
        """GET /account/login | anonymous user | user is None"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.LOGIN_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        res: HttpResponse = self.client.post(self.LOGIN_URL, {'username': 'fake_user', 'passphrase': 'passphrase', 'email': 'email@example.com'}, follow=True)
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

    GET /account/login | authenticated user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /account/login | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.LOGIN_URL)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))
        res: HttpResponse = self.client.get(self.LOGIN_URL, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    GET /account/logout | anonymous user

??? example "Snippet"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /account/logout | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.LOGOUT_URL)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.LOGIN_URL + '?next=' + self.LOGOUT_URL)
        res: HttpResponse = self.client.get(self.LOGOUT_URL, follow=True)
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

    GET /account/logout | anonymous user

??? example "Snippet"

    ```py
    def test_GET_authenticated_user(self) -> None:
        """GET /account/logout | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(self.LOGOUT_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/logout.html')
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

    POST /account/logout | anonymous user

??? example "Snippet"

    ```py
    def test_POST_authenticated_user(self) -> None:
        """POST /account/logout | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.post(self.LOGOUT_URL)
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(self.client.login(username='user', passphrase='passphrase'))
        res: HttpResponse = self.client.post(self.LOGOUT_URL, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
