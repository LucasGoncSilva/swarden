
# File: `test_models.py`
Path: `SWARDEN.honeypot.tests`



---

## Imports

### `#!py import datetime`

Path: `#!py datetime`

Category: Native

??? example "SNIPPET"

    ```py
    from datetime import datetime
    ```

### `#!py import filterwarnings`

Path: `#!py warnings`

Category: Native

??? example "SNIPPET"

    ```py
    from warnings import filterwarnings
    ```

### `#!py import ValidationError`

Path: `#!py django.core.exceptions`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.exceptions import ValidationError
    ```

### `#!py import atomic`

Path: `#!py django.db.transaction`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.transaction import atomic
    ```

### `#!py import TestCase`

Path: `#!py django.test`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.test import TestCase
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

### `#!py class AttemptTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class AttemptTestCase(TestCase):

        def setUp(self) -> None:
            filterwarnings('ignore', category=RuntimeWarning)
            self.attempt1: Attempt = Attempt.objects.create(IP='255.255.255.255', username='username', password='password', URL='<script>alert(1)</script>', timestamp=datetime(2017, 7, 8))
            self.attempt2: Attempt = Attempt.objects.create(IP='0' * 64, username='u' * 256, password='p' * 256, URL='!' * 256)
            self.attempt3: Attempt = Attempt.objects.create(IP='0' * 64, username='u' * 256, password='p' * 256, URL='!' * 256, timestamp='string')
            self.attempt4: Attempt = Attempt.objects.create(IP='0' * 64, password='p' * 256, URL='!' * 256)
            self.attempt5: Attempt = Attempt.objects.create(username='u' * 256, password='p' * 256, URL='!' * 256)

        def test_attempt_instance_validity(self) -> None:
            """Tests attempt instance of correct class"""
            for attempt in Attempt.objects.all():
                with self.subTest(attempt=attempt):
                    self.assertIsInstance(attempt, Attempt)

        def test_attempt_special_str_method_return(self) -> None:
            """Tests attempt return value of __str__ method"""
            attempt1: Attempt = Attempt.objects.get(pk=self.attempt1.pk)
            date: datetime = attempt1.timestamp
            d: int = date.day
            m: int = date.month
            y: int = date.year
            h: int = date.hour
            min: int = date.minute
            s: int = date.second
            self.assertEqual(attempt1.__str__(), f'{attempt1.pk}: {d}/{m}/{y} ({h}h{min}m{s}s) UTC+3')

        def test_attempt_key_value_assertion(self) -> None:
            """Tests attempt correct attribuition of value"""
            attempt1: Attempt = Attempt.objects.get(pk=self.attempt1.pk)
            self.assertEqual(attempt1.IP, '255.255.255.255')
            self.assertEqual(attempt1.username, 'username')
            self.assertEqual(attempt1.password, 'password')
            self.assertEqual(attempt1.URL, '<script>alert(1)</script>')
            self.assertNotEqual(attempt1.timestamp, datetime(2017, 7, 8))

        def test_attempt_create_validity(self) -> None:
            """Tests attempt creation integrity and validation"""
            attempt1: Attempt = Attempt.objects.get(pk=self.attempt1.pk)
            attempt2: Attempt = Attempt.objects.get(pk=self.attempt2.pk)
            attempt3: Attempt = Attempt.objects.get(pk=self.attempt3.pk)
            attempt4: Attempt = Attempt.objects.get(pk=self.attempt4.pk)
            attempt5: Attempt = Attempt.objects.get(pk=self.attempt5.pk)
            self.assertEqual(Attempt.objects.all().count(), 5)
            self.assertTrue(attempt1.is_valid())
            self.assertTrue(attempt2.is_valid())
            self.assertTrue(attempt3.is_valid())
            self.assertFalse(attempt4.is_valid())
            self.assertFalse(attempt5.is_valid())

        def test_attempt_update_validity(self) -> None:
            """Tests attempt update integrity and validation"""
            Attempt.objects.filter(pk=self.attempt4.pk).update(username='bob_a_bob')
            Attempt.objects.filter(pk=self.attempt5.pk).update(IP='192.168.55.36')
            for attempt in Attempt.objects.all():
                with self.subTest(attempt=attempt):
                    self.assertTrue(attempt.is_valid())

        def test_attempt_delete_validity(self) -> None:
            """Tests attempt correct deletion"""
            for attempt in Attempt.objects.all():
                if not attempt.is_valid():
                    attempt.delete()
            self.assertEqual(Attempt.objects.all().count(), 3)

        def test_attempt_db_exception_raises(self) -> None:
            """Tests attempt correct integrity and validation with raised exceptions"""
            raise_kwargs: dict[str, dict[str, str | None]] = {'attemp1': {'IP': 'foobarbazqux'}, 'attemp2': {'IP': 'x' * 65}, 'attemp3': {'IP': None}, 'attemp4': {'username': 'foobarbazqux'}, 'attemp5': {'username': 'x' * 257}, 'attemp6': {'username': None}, 'attemp7': {'password': 'foobarbazqux'}, 'attemp8': {'password': 'x' * 257}, 'attemp9': {'password': None}, 'attemp10': {'URL': 'foobarbazqux'}, 'attemp11': {'URL': 'x' * 257}, 'attemp12': {'URL': None}, 'attemp13': {'timestamp': 'foobarbazqux'}, 'attemp14': {'timestamp': None}}
            for scenario in raise_kwargs.keys():
                with self.subTest(scenario=scenario):
                    with self.assertRaises(ValidationError):
                        with atomic():
                            instance: Attempt = Attempt(**raise_kwargs[scenario])
                            instance.full_clean()
            no_raise_kwargs: dict[str, dict[str, str | int | datetime]] = {'attemp1': {'IP': '255.255.255.255', 'username': 'username', 'password': 'password', 'URL': 'URL'}, 'attemp2': {'IP': '255.255.255.255', 'username': 'username', 'password': 'password', 'URL': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'timestamp': datetime(1980, 4, 25)}, 'attemp3': {'IP': '255.255.255.255', 'username': 10 ** 255, 'password': 10 ** 255, 'URL': '<script>alert(404)</script>', 'timestamp': '2023-10-15'}, 'attemp4': {'IP': 'x' * 64, 'username': 'x' * 256, 'password': 'x' * 256, 'URL': 'x' * 256, 'timestamp': datetime(2023, 10, 15)}}
            for scenario in no_raise_kwargs.keys():
                with self.subTest(scenario=scenario):
                    instance: Attempt = Attempt(**no_raise_kwargs[scenario])
                    instance.full_clean()
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
        filterwarnings('ignore', category=RuntimeWarning)
        self.attempt1: Attempt = Attempt.objects.create(IP='255.255.255.255', username='username', password='password', URL='<script>alert(1)</script>', timestamp=datetime(2017, 7, 8))
        self.attempt2: Attempt = Attempt.objects.create(IP='0' * 64, username='u' * 256, password='p' * 256, URL='!' * 256)
        self.attempt3: Attempt = Attempt.objects.create(IP='0' * 64, username='u' * 256, password='p' * 256, URL='!' * 256, timestamp='string')
        self.attempt4: Attempt = Attempt.objects.create(IP='0' * 64, password='p' * 256, URL='!' * 256)
        self.attempt5: Attempt = Attempt.objects.create(username='u' * 256, password='p' * 256, URL='!' * 256)
    ```

### `#!py def test_attempt_instance_validity`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_instance_validity(self) -> None:
        """Tests attempt instance of correct class"""
        for attempt in Attempt.objects.all():
            with self.subTest(attempt=attempt):
                self.assertIsInstance(attempt, Attempt)
    ```

### `#!py def test_attempt_special_str_method_return`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_special_str_method_return(self) -> None:
        """Tests attempt return value of __str__ method"""
        attempt1: Attempt = Attempt.objects.get(pk=self.attempt1.pk)
        date: datetime = attempt1.timestamp
        d: int = date.day
        m: int = date.month
        y: int = date.year
        h: int = date.hour
        min: int = date.minute
        s: int = date.second
        self.assertEqual(attempt1.__str__(), f'{attempt1.pk}: {d}/{m}/{y} ({h}h{min}m{s}s) UTC+3')
    ```

### `#!py def test_attempt_key_value_assertion`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_key_value_assertion(self) -> None:
        """Tests attempt correct attribuition of value"""
        attempt1: Attempt = Attempt.objects.get(pk=self.attempt1.pk)
        self.assertEqual(attempt1.IP, '255.255.255.255')
        self.assertEqual(attempt1.username, 'username')
        self.assertEqual(attempt1.password, 'password')
        self.assertEqual(attempt1.URL, '<script>alert(1)</script>')
        self.assertNotEqual(attempt1.timestamp, datetime(2017, 7, 8))
    ```

### `#!py def test_attempt_create_validity`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_create_validity(self) -> None:
        """Tests attempt creation integrity and validation"""
        attempt1: Attempt = Attempt.objects.get(pk=self.attempt1.pk)
        attempt2: Attempt = Attempt.objects.get(pk=self.attempt2.pk)
        attempt3: Attempt = Attempt.objects.get(pk=self.attempt3.pk)
        attempt4: Attempt = Attempt.objects.get(pk=self.attempt4.pk)
        attempt5: Attempt = Attempt.objects.get(pk=self.attempt5.pk)
        self.assertEqual(Attempt.objects.all().count(), 5)
        self.assertTrue(attempt1.is_valid())
        self.assertTrue(attempt2.is_valid())
        self.assertTrue(attempt3.is_valid())
        self.assertFalse(attempt4.is_valid())
        self.assertFalse(attempt5.is_valid())
    ```

### `#!py def test_attempt_update_validity`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_update_validity(self) -> None:
        """Tests attempt update integrity and validation"""
        Attempt.objects.filter(pk=self.attempt4.pk).update(username='bob_a_bob')
        Attempt.objects.filter(pk=self.attempt5.pk).update(IP='192.168.55.36')
        for attempt in Attempt.objects.all():
            with self.subTest(attempt=attempt):
                self.assertTrue(attempt.is_valid())
    ```

### `#!py def test_attempt_delete_validity`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_delete_validity(self) -> None:
        """Tests attempt correct deletion"""
        for attempt in Attempt.objects.all():
            if not attempt.is_valid():
                attempt.delete()
        self.assertEqual(Attempt.objects.all().count(), 3)
    ```

### `#!py def test_attempt_db_exception_raises`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_attempt_db_exception_raises(self) -> None:
        """Tests attempt correct integrity and validation with raised exceptions"""
        raise_kwargs: dict[str, dict[str, str | None]] = {'attemp1': {'IP': 'foobarbazqux'}, 'attemp2': {'IP': 'x' * 65}, 'attemp3': {'IP': None}, 'attemp4': {'username': 'foobarbazqux'}, 'attemp5': {'username': 'x' * 257}, 'attemp6': {'username': None}, 'attemp7': {'password': 'foobarbazqux'}, 'attemp8': {'password': 'x' * 257}, 'attemp9': {'password': None}, 'attemp10': {'URL': 'foobarbazqux'}, 'attemp11': {'URL': 'x' * 257}, 'attemp12': {'URL': None}, 'attemp13': {'timestamp': 'foobarbazqux'}, 'attemp14': {'timestamp': None}}
        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: Attempt = Attempt(**raise_kwargs[scenario])
                        instance.full_clean()
        no_raise_kwargs: dict[str, dict[str, str | int | datetime]] = {'attemp1': {'IP': '255.255.255.255', 'username': 'username', 'password': 'password', 'URL': 'URL'}, 'attemp2': {'IP': '255.255.255.255', 'username': 'username', 'password': 'password', 'URL': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'timestamp': datetime(1980, 4, 25)}, 'attemp3': {'IP': '255.255.255.255', 'username': 10 ** 255, 'password': 10 ** 255, 'URL': '<script>alert(404)</script>', 'timestamp': '2023-10-15'}, 'attemp4': {'IP': 'x' * 64, 'username': 'x' * 256, 'password': 'x' * 256, 'URL': 'x' * 256, 'timestamp': datetime(2023, 10, 15)}}
        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: Attempt = Attempt(**no_raise_kwargs[scenario])
                instance.full_clean()
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
