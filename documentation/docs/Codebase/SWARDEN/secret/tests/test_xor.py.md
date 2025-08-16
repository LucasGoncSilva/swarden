# File: `test_xor.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret.tests`

No file docstring provided.

---

## Imports

### `#!py import queue`

Path: `#!py None`

Category: native

??? example "Snippet"

    ```py
    import queue
    ```

### `#!py import threading`

Path: `#!py None`

Category: native

??? example "Snippet"

    ```py
    import threading
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```

### `#!py import TestCase`

Path: `#!py django.test`

Category: trdparty

??? example "Snippet"

    ```py
    from django.test import TestCase
    ```

### `#!py import xor`

Path: `#!py utils`

Category: trdparty

??? example "Snippet"

    ```py
    from utils import xor
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class XORTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class XORTestCase(TestCase):

        def setUp(self) -> None:
            self.passphrase = User.objects.create_user(username='user', passphrase='testing_passphrase', email='user@example.com').passphrase
            self.q: queue.Queue = queue.Queue()
            self.num = 100000

        def test_xor_return_values(self) -> None:
            """Tests raises and return values"""
            self.assertIsNone(xor(None, self.passphrase[21:]))
            self.assertEqual(xor('', self.passphrase[21:]), '')
            self.assertEqual(xor(5, self.passphrase[21:]), 5)

        def test_xor_null_value(self) -> None:
            """Tests return values"""
            with open('secret/tests/sample.txt') as txt:
                lines: list[str] = txt.readlines()
                for line in lines:
                    data: str = line.strip()
                    encrypted_data: str = xor(data, self.passphrase[21:])
                    decrypted_data: str = xor(encrypted_data, self.passphrase[21:], encrypt=False)
                    self.q.put(encrypted_data)
                    self.q.put(decrypted_data)
            threading.Thread(target=self.process_xor, daemon=True).start()
            self.q.join()

        def process_xor(self) -> None:
            while True:
                data = self.q.get()
                self.assertNotIn('\x00', data)
                self.assertTrue(all(map(lambda x: x in range(1114112), [ord(i) for i in data])))
                self.q.task_done()
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
        self.passphrase = User.objects.create_user(username='user', passphrase='testing_passphrase', email='user@example.com').passphrase
        self.q: queue.Queue = queue.Queue()
        self.num = 100000
    ```

### `#!py def test_xor_return_values`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    Tests raises and return values

??? example "Snippet"

    ```py
    def test_xor_return_values(self) -> None:
        """Tests raises and return values"""
        self.assertIsNone(xor(None, self.passphrase[21:]))
        self.assertEqual(xor('', self.passphrase[21:]), '')
        self.assertEqual(xor(5, self.passphrase[21:]), 5)
    ```

### `#!py def test_xor_null_value`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    Tests return values

??? example "Snippet"

    ```py
    def test_xor_null_value(self) -> None:
        """Tests return values"""
        with open('secret/tests/sample.txt') as txt:
            lines: list[str] = txt.readlines()
            for line in lines:
                data: str = line.strip()
                encrypted_data: str = xor(data, self.passphrase[21:])
                decrypted_data: str = xor(encrypted_data, self.passphrase[21:], encrypt=False)
                self.q.put(encrypted_data)
                self.q.put(decrypted_data)
        threading.Thread(target=self.process_xor, daemon=True).start()
        self.q.join()
    ```

### `#!py def process_xor`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def process_xor(self) -> None:
        while True:
            data = self.q.get()
            self.assertNotIn('\x00', data)
            self.assertTrue(all(map(lambda x: x in range(1114112), [ord(i) for i in data])))
            self.q.task_done()
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
