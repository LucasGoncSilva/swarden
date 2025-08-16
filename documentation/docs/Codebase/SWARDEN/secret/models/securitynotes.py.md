# File: `securitynotes.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.secret.models`

No file docstring provided.

---

## Imports

### `#!py import Final`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Final
    ```

### `#!py import uuid4`

Path: `#!py uuid`

Category: native

??? example "Snippet"

    ```py
    from uuid import uuid4
    ```

### `#!py import User`

Path: `#!py account.models`

Category: trdparty

??? example "Snippet"

    ```py
    from account.models import User
    ```

### `#!py import MaxLengthValidator`

Path: `#!py django.core.validators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core.validators import MaxLengthValidator
    ```

### `#!py import MinLengthValidator`

Path: `#!py django.core.validators`

Category: trdparty

??? example "Snippet"

    ```py
    from django.core.validators import MinLengthValidator
    ```

### `#!py import CASCADE`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import CASCADE
    ```

### `#!py import CharField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import CharField
    ```

### `#!py import DateTimeField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import DateTimeField
    ```

### `#!py import ForeignKey`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import ForeignKey
    ```

### `#!py import Model`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import Model
    ```

### `#!py import SlugField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import SlugField
    ```

### `#!py import TextField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import TextField
    ```

### `#!py import UUIDField`

Path: `#!py django.db.models`

Category: trdparty

??? example "Snippet"

    ```py
    from django.db.models import UUIDField
    ```

### `#!py import slugify`

Path: `#!py django.template.defaultfilters`

Category: trdparty

??? example "Snippet"

    ```py
    from django.template.defaultfilters import slugify
    ```

### `#!py import reverse`

Path: `#!py django.urls`

Category: trdparty

??? example "Snippet"

    ```py
    from django.urls import reverse
    ```

### `#!py import xor`

Path: `#!py utils`

Category: trdparty

??? example "Snippet"

    ```py
    from utils import xor
    ```

### `#!py import notes_types`

Path: `#!py secret.choices`

Category: trdparty

??? example "Snippet"

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

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class SecurityNote(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        owner: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE, related_name='notes')
        title: Final[CharField] = CharField(max_length=40, validators=[MaxLengthValidator(40)])
        content: TextField = TextField(max_length=1000, validators=[MaxLengthValidator(1000)])
        note_type: Final[TextField] = TextField(max_length=3, choices=notes_types, validators=[MaxLengthValidator(3), MinLengthValidator(3)])
        slug: Final[SlugField] = SlugField(max_length=50, validators=[MaxLengthValidator(50)])
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
        updated: Final[DateTimeField] = DateTimeField(auto_now=True)

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
    ```

### `#!py class Meta`

Parents: `None`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class Meta:
        ordering: Final[list[str]] = ['-created']
    ```



---

## Functions

### `#!py def __str__`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def __str__(self) -> str:
        return f'{str(self.owner.username)} | {self.title}'
    ```

### `#!py def get_absolute_url`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py str`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def get_absolute_url(self) -> str:
        return reverse('secret:note_list_view')
    ```

### `#!py def save`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, force_insert: Unknown, force_update: Unknown, using: Unknown, update_fields: Unknown`

Kwargs: `#!py None`

Return Type: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.content = xor(str(self.content), self.owner.password[21:])
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
    ```

### `#!py def from_db`

Type: `#!py method`

Decorators: `#!py classmethod`

Args: `#!py cls: Unknown, db: Unknown, field_names: Unknown, values: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    @classmethod
    def from_db(cls, db, field_names, values):
        note: SecurityNote = super().from_db(db, field_names, values)
        note.content = xor(str(note.content), note.owner.password[21:], encrypt=False)
        return note
    ```

### `#!py def expected_max_length`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, var: str`

Kwargs: `#!py None`

Return Type: `#!py int`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def expected_max_length(self, var: str) -> int:
        max_length: Final[dict[str, int]] = {'title': 40, 'content': 300, 'note_type': 3, 'slug': 50}
        return max_length[var]
    ```

### `#!py def check_field_length`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, var: str`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def check_field_length(self, var: str) -> bool:
        value = self.__getattribute__(var)
        return len(value) <= self.expected_max_length(var)
    ```

### `#!py def all_fields_of_right_length`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def all_fields_of_right_length(self) -> bool:
        vars: Final[list[str]] = ['title', 'content', 'note_type', 'slug']
        return all(map(self.check_field_length, vars))
    ```

### `#!py def all_fields_present`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def all_fields_present(self) -> bool:
        return bool(self.owner and self.title and self.content and self.note_type and (self.slug == slugify(str(self.title))))
    ```

### `#!py def all_fields_of_correct_types`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def all_fields_of_correct_types(self) -> bool:
        return [str(type(self.owner)), type(self.title), type(self.content), type(self.note_type), type(self.slug)] == ["<class 'account.models.User'>", str, str, str, str]
    ```

### `#!py def is_valid`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py bool`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def is_valid(self) -> bool:
        if self.all_fields_present() and self.all_fields_of_correct_types() and self.all_fields_of_right_length():
            return True
        return False
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
