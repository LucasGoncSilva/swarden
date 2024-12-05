
# File: `test_xor.py`
Path: `SWARDEN.secret.tests`



---

## Imports

### `#!py import queue`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import queue
    ```

### `#!py import threading`

Path: `#!py None`

Category: Native

??? example "SNIPPET"

    ```py
    import threading
    ```

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```

### `#!py import TestCase`

Path: `#!py django.test`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.test import TestCase
    ```

### `#!py import xor`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

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

??? example "SNIPPET"

    ```py
    class XORTestCase(TestCase):

        def setUp(self) -> None:
            self.password = User.objects.create_user(username='user', password='testing_password', email='user@example.com').password
            self.q: queue.Queue = queue.Queue()
            self.num = 100000

        def test_xor_return_values(self) -> None:
            """Tests raises and return values"""
            self.assertIsNone(xor(None, self.password[21:]))
            self.assertEqual(xor('', self.password[21:]), '')
            self.assertEqual(xor(5, self.password[21:]), 5)

        def test_xor_null_value(self) -> None:
            """Tests return values"""
            with open('secret/tests/sample.txt') as txt:
                lines: list[str] = txt.readlines()
                for line in lines:
                    data: str = line.strip()
                    encrypted_data: str = xor(data, self.password[21:])
                    decrypted_data: str = xor(encrypted_data, self.password[21:], encrypt=False)
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

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def setUp(self) -> None:
        self.password = User.objects.create_user(username='user', password='testing_password', email='user@example.com').password
        self.q: queue.Queue = queue.Queue()
        self.num = 100000
    ```

### `#!py def test_xor_return_values`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_xor_return_values(self) -> None:
        """Tests raises and return values"""
        self.assertIsNone(xor(None, self.password[21:]))
        self.assertEqual(xor('', self.password[21:]), '')
        self.assertEqual(xor(5, self.password[21:]), 5)
    ```

### `#!py def test_xor_null_value`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_xor_null_value(self) -> None:
        """Tests return values"""
        with open('secret/tests/sample.txt') as txt:
            lines: list[str] = txt.readlines()
            for line in lines:
                data: str = line.strip()
                encrypted_data: str = xor(data, self.password[21:])
                decrypted_data: str = xor(encrypted_data, self.password[21:], encrypt=False)
                self.q.put(encrypted_data)
                self.q.put(decrypted_data)
        threading.Thread(target=self.process_xor, daemon=True).start()
        self.q.join()
    ```

### `#!py def process_xor`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

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
