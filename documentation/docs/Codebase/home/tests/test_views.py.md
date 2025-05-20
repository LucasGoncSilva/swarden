
# File: `test_views.py`
Path: `SWARDEN.home.tests`



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

### `#!py import Card`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import Card
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.models import SecurityNote
    ```

### `#!py import Month`

Path: `#!py secret.month.models`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.month.models import Month
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class HomeViewsTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class HomeViewsTestCase(TestCase):

        def setUp(self) -> None:
            user: User = User.objects.create_user(username='user', password='password', email='user@email.com')
            Card.objects.create(owner=user, name='Personal Main Card', card_type='deb', number='4002892240028922', expiration=Month(2028, 11), cvv='113', bank='nubank--', brand='mastercard--', slug='nubank--personal-main-card', owners_name='TEST USER')
            LoginCredential.objects.create(owner=user, service='google--', name='Personal Main Account', slug='google--personal-main-account', third_party_login=False, third_party_login_name='-----', login='night_monkey123@gmail.com', password='ilovemenotyou')
            LoginCredential.objects.create(owner=user, service='steam--', name='Little Fries', slug='steam--little-fries', third_party_login=True, third_party_login_name='Personal Main Account', login='-----', password='-----')
            SecurityNote.objects.create(owner=user, title='How to draw an apple', slug='how-to-draw-an-apple', content='Just draw an apple tree and erase the tree.')

        def test_GET_anonymous_user(self):
            """GET / | anonymous user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            res: HttpResponse = self.client.get(reverse('home:index'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/landing.html')
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)

        def test_GET_authenticated_user(self):
            """GET / | authenticated user"""
            self.assertTrue(get_user(self.client).is_anonymous)
            self.assertFalse(get_user(self.client).is_authenticated)
            self.client.login(username='user', password='password')
            res: HttpResponse = self.client.get(reverse('home:index'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'home/index.html')
            self.assertIn('cards', res.context.keys())
            self.assertIn('credentials', res.context.keys())
            self.assertIn('notes', res.context.keys())
            self.assertEqual(len(res.context['cards']), 1)
            self.assertEqual(len(res.context['credentials']), 2)
            self.assertEqual(len(res.context['notes']), 1)
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
        user: User = User.objects.create_user(username='user', password='password', email='user@email.com')
        Card.objects.create(owner=user, name='Personal Main Card', card_type='deb', number='4002892240028922', expiration=Month(2028, 11), cvv='113', bank='nubank--', brand='mastercard--', slug='nubank--personal-main-card', owners_name='TEST USER')
        LoginCredential.objects.create(owner=user, service='google--', name='Personal Main Account', slug='google--personal-main-account', third_party_login=False, third_party_login_name='-----', login='night_monkey123@gmail.com', password='ilovemenotyou')
        LoginCredential.objects.create(owner=user, service='steam--', name='Little Fries', slug='steam--little-fries', third_party_login=True, third_party_login_name='Personal Main Account', login='-----', password='-----')
        SecurityNote.objects.create(owner=user, title='How to draw an apple', slug='how-to-draw-an-apple', content='Just draw an apple tree and erase the tree.')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user(self):
        """GET / | anonymous user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        res: HttpResponse = self.client.get(reverse('home:index'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
    ```

### `#!py def test_GET_authenticated_user`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_authenticated_user(self):
        """GET / | authenticated user"""
        self.assertTrue(get_user(self.client).is_anonymous)
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username='user', password='password')
        res: HttpResponse = self.client.get(reverse('home:index'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertIn('cards', res.context.keys())
        self.assertIn('credentials', res.context.keys())
        self.assertIn('notes', res.context.keys())
        self.assertEqual(len(res.context['cards']), 1)
        self.assertEqual(len(res.context['credentials']), 2)
        self.assertEqual(len(res.context['notes']), 1)
        self.assertFalse(get_user(self.client).is_anonymous)
        self.assertTrue(get_user(self.client).is_authenticated)
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
