
# File: `test_views.py`
Path: `SWARDEN.err.tests`



---

## Imports

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



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class Error403ViewTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Error403ViewTestCase(TestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /erro/403"""
            res: HttpResponse = self.client.get(reverse('err:403'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertEqual(res.context.get('code'), 403)
            self.assertEqual(res.context.get('message1'), 'Você não tem autorização para proseguir.')
            self.assertEqual(res.context.get('message2'), 'Retorne para onde estava ou vá para a homepage.')
    ```

### `#!py class Error404ViewTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Error404ViewTestCase(TestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /erro/404"""
            res: HttpResponse = self.client.get(reverse('err:404'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertEqual(res.context.get('code'), 404)
            self.assertEqual(res.context.get('message1'), 'O endereço requisitado não foi encontrado.')
            self.assertEqual(res.context.get('message2'), 'Retorne para onde estava ou vá para a homepage.')
    ```

### `#!py class Error500ViewTestCase`

Parents: `TestCase`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Error500ViewTestCase(TestCase):

        def test_GET_anonymous_user(self) -> None:
            """GET /erro/500"""
            res: HttpResponse = self.client.get(reverse('err:500'))
            self.assertEqual(res.status_code, 200)
            self.assertTemplateUsed(res, 'err/error_template.html')
            self.assertEqual(res.context.get('code'), 500)
            self.assertEqual(res.context.get('message1'), 'Ocorreu um problema com o servidor.')
            self.assertEqual(res.context.get('message2'), 'Informe o problema para a equipe do site.')
    ```



---

## Functions

### `#!py def test_GET_anonymous_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /erro/403"""
        res: HttpResponse = self.client.get(reverse('err:403'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context.get('code'), 403)
        self.assertEqual(res.context.get('message1'), 'Você não tem autorização para proseguir.')
        self.assertEqual(res.context.get('message2'), 'Retorne para onde estava ou vá para a homepage.')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /erro/404"""
        res: HttpResponse = self.client.get(reverse('err:404'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context.get('code'), 404)
        self.assertEqual(res.context.get('message1'), 'O endereço requisitado não foi encontrado.')
        self.assertEqual(res.context.get('message2'), 'Retorne para onde estava ou vá para a homepage.')
    ```

### `#!py def test_GET_anonymous_user`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def test_GET_anonymous_user(self) -> None:
        """GET /erro/500"""
        res: HttpResponse = self.client.get(reverse('err:500'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'err/error_template.html')
        self.assertEqual(res.context.get('code'), 500)
        self.assertEqual(res.context.get('message1'), 'Ocorreu um problema com o servidor.')
        self.assertEqual(res.context.get('message2'), 'Informe o problema para a equipe do site.')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
