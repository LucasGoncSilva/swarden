
# File: `securitynotes.py`
Path: `SWARDEN.secret.models`



---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: Native

??? example "SNIPPET"

    ```py
    from typing import Final
    ```

### `#!py import uuid4`

Path: `#!py uuid`

Category: Native

??? example "SNIPPET"

    ```py
    from uuid import uuid4
    ```

### `#!py import User`

Path: `#!py account.models`

Category: Local

??? example "SNIPPET"

    ```py
    from account.models import User
    ```

### `#!py import MaxLengthValidator`

Path: `#!py django.core.validators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.validators import MaxLengthValidator
    ```

### `#!py import MinLengthValidator`

Path: `#!py django.core.validators`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.core.validators import MinLengthValidator
    ```

### `#!py import CASCADE`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import CASCADE
    ```

### `#!py import CharField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import CharField
    ```

### `#!py import DateTimeField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import DateTimeField
    ```

### `#!py import ForeignKey`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import ForeignKey
    ```

### `#!py import Model`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import Model
    ```

### `#!py import SlugField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import SlugField
    ```

### `#!py import TextField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import TextField
    ```

### `#!py import UUIDField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import UUIDField
    ```

### `#!py import slugify`

Path: `#!py django.template.defaultfilters`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.template.defaultfilters import slugify
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.urls import reverse
    ```

### `#!py import xor`

Path: `#!py utils`

Category: Local

??? example "SNIPPET"

    ```py
    from utils import xor
    ```

### `#!py import notes_types`

Path: `#!py secret.choices`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.choices import notes_types
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class SecurityNote`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class SecurityNote(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        owner: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE, related_name='notes', verbose_name='Dono')
        title: Final[CharField] = CharField(max_length=40, verbose_name='Título', validators=[MaxLengthValidator(40)])
        content: TextField = TextField(max_length=300, verbose_name='Conteúdo', validators=[MaxLengthValidator(300)])
        note_type: Final[TextField] = TextField(max_length=3, choices=notes_types, verbose_name='Classificação', validators=[MaxLengthValidator(3), MinLengthValidator(3)])
        slug: Final[SlugField] = SlugField(max_length=50, validators=[MaxLengthValidator(50)])
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True, verbose_name='Criado em')
        updated: Final[DateTimeField] = DateTimeField(auto_now=True, verbose_name='Atualizado em')

        def __str__(self) -> str:
            return f'{str(self.owner.username)} | {self.title}'

        def get_absolute_url(self) -> str:
            return reverse('secret:note_list_view')

        def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
            self.content = xor(str(self.content), self.owner.password[21:])
            return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

        @classmethod
        def from_db(cls, db, field_names, values):
            note: SecurityNote = super().from_db(db, field_names, values)
            note.content = xor(str(note.content), note.owner.password[21:], encrypt=False)
            return note

        def expected_max_length(self, var: str) -> int:
            max_length: Final[dict[str, int]] = {'title': 40, 'content': 300, 'note_type': 3, 'slug': 50}
            return max_length[var]

        def check_field_length(self, var: str) -> bool:
            value = self.__getattribute__(var)
            return len(value) <= self.expected_max_length(var)

        def all_fields_of_right_length(self) -> bool:
            vars: Final[list[str]] = ['title', 'content', 'note_type', 'slug']
            return all(map(self.check_field_length, vars))

        def all_fields_present(self) -> bool:
            return bool(self.owner and self.title and self.content and self.note_type and (self.slug == slugify(str(self.title))))

        def all_fields_of_correct_types(self) -> bool:
            return [str(type(self.owner)), type(self.title), type(self.content), type(self.note_type), type(self.slug)] == ["<class 'account.models.User'>", str, str, str, str]

        def is_valid(self) -> bool:
            if self.all_fields_present() and self.all_fields_of_correct_types() and self.all_fields_of_right_length():
                return True
            return False

        class Meta:
            ordering: Final[list[str]] = ['-created']
            verbose_name: Final[str] = 'Nota de Segurança'
            verbose_name_plural: Final[str] = 'Notas de Segurança'
    ```

### `#!py class Meta`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Meta:
        ordering: Final[list[str]] = ['-created']
        verbose_name: Final[str] = 'Nota de Segurança'
        verbose_name_plural: Final[str] = 'Notas de Segurança'
    ```



---

## Functions

### `#!py def __str__`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def __str__(self) -> str:
        return f'{str(self.owner.username)} | {self.title}'
    ```

### `#!py def get_absolute_url`

Type: `#!py ...`

Return Type: `#!py str`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def get_absolute_url(self) -> str:
        return reverse('secret:note_list_view')
    ```

### `#!py def save`

Type: `#!py ...`

Return Type: `#!py None`

Decorators: `#!py None`

Args: `#!py self: Unknown, force_insert: Unknown, force_update: Unknown, using: Unknown, update_fields: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.content = xor(str(self.content), self.owner.password[21:])
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
    ```

### `#!py def from_db`

Type: `#!py ...`

Return Type: `#!py Unknown`

Decorators: `#!py classmethod`

Args: `#!py cls: Unknown, db: Unknown, field_names: Unknown, values: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    @classmethod
    def from_db(cls, db, field_names, values):
        note: SecurityNote = super().from_db(db, field_names, values)
        note.content = xor(str(note.content), note.owner.password[21:], encrypt=False)
        return note
    ```

### `#!py def expected_max_length`

Type: `#!py ...`

Return Type: `#!py int`

Decorators: `#!py None`

Args: `#!py self: Unknown, var: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {'title': 40, 'content': 300, 'note_type': 3, 'slug': 50}
        return max_length[var]
    ```

### `#!py def check_field_length`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown, var: str`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)
        return len(value) <= self.expected_max_length(var)
    ```

### `#!py def all_fields_of_right_length`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = ['title', 'content', 'note_type', 'slug']
        return all(map(self.check_field_length, vars))
    ```

### `#!py def all_fields_present`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def all_fields_present(self) -> bool:
        return bool(self.owner and self.title and self.content and self.note_type and (self.slug == slugify(str(self.title))))
    ```

### `#!py def all_fields_of_correct_types`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def all_fields_of_correct_types(self) -> bool:
        return [str(type(self.owner)), type(self.title), type(self.content), type(self.note_type), type(self.slug)] == ["<class 'account.models.User'>", str, str, str, str]
    ```

### `#!py def is_valid`

Type: `#!py ...`

Return Type: `#!py bool`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    def is_valid(self) -> bool:
        if self.all_fields_present() and self.all_fields_of_correct_types() and self.all_fields_of_right_length():
            return True
        return False
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
