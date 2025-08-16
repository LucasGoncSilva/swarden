# File: `card.py`

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

### `#!py import cards_banks`

Path: `#!py secret.choices`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.choices import cards_banks
    ```

### `#!py import cards_brands`

Path: `#!py secret.choices`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.choices import cards_brands
    ```

### `#!py import cards_types`

Path: `#!py secret.choices`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.choices import cards_types
    ```

### `#!py import MonthField`

Path: `#!py secret.month.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.month.models import MonthField
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class PaymentCard`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class PaymentCard(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        owner: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE, related_name='cards')
        name: CharField = CharField(max_length=40, validators=[MaxLengthValidator(40)])
        card_type: CharField = CharField(max_length=4, choices=cards_types, validators=[MaxLengthValidator(4)])
        number: CharField = CharField(max_length=19, validators=[MinLengthValidator(12), MaxLengthValidator(19)])
        expiration = MonthField()
        cvv: CharField = CharField(max_length=4, validators=[MinLengthValidator(3), MaxLengthValidator(4)])
        bank: CharField = CharField(max_length=64, choices=cards_banks)
        brand: CharField = CharField(max_length=64, choices=cards_brands)
        owners_name: CharField = CharField(max_length=64, validators=[MaxLengthValidator(64)])
        note: TextField = TextField(max_length=128, blank=True, null=True, validators=[MaxLengthValidator(128)])
        slug: Final[SlugField] = SlugField(max_length=128, validators=[MaxLengthValidator(128)])
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True)
        updated: Final[DateTimeField] = DateTimeField(auto_now=True)

        class Meta:
            ordering: Final[list[str]] = ['-created']

        def __str__(self) -> str:
            return f'{str(self.owner.username)} | {self.card_type} | {self.name}'

        def get_absolute_url(self) -> str:
            return reverse('secret:card_list_view')

        def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
            self.name = xor(str(self.name), self.owner.password[21:])
            self.number = xor(str(self.number), self.owner.password[21:])
            self.cvv = xor(str(self.cvv), self.owner.password[21:])
            self.owners_name = xor(str(self.owners_name), self.owner.password[21:])
            self.note = xor(str(self.note), self.owner.password[21:])
            return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

        @classmethod
        def from_db(cls, db, field_names, values):
            card: PaymentCard = super().from_db(db, field_names, values)
            card.name = xor(str(card.name), card.owner.password[21:], encrypt=False)
            card.number = xor(str(card.number), card.owner.password[21:], encrypt=False)
            card.cvv = xor(str(card.cvv), card.owner.password[21:], encrypt=False)
            card.owners_name = xor(str(card.owners_name), card.owner.password[21:], encrypt=False)
            card.note = xor(str(card.note), card.owner.password[21:], encrypt=False)
            return card

        def expected_max_length(self, var: str) -> int:
            max_length: Final[dict[str, int]] = {'name': 40, 'card_type': 16, 'number': 19, 'cvv': 4, 'bank': 64, 'brand': 64, 'slug': 128, 'owners_name': 64, 'note': 128}
            return max_length[var]

        def expected_min_length(self, var: str) -> int:
            min_length: Final[dict[str, int]] = {'number': 12, 'cvv': 3}
            return min_length[var]

        def check_field_length(self, var: str) -> bool:
            if var == 'expiration':
                return True
            value = self.__getattribute__(var)
            if var in ['number', 'cvv']:
                return self.expected_min_length(var) <= len(value) <= self.expected_max_length(var)
            return len(value) <= self.expected_max_length(var)

        def all_fields_of_right_length(self) -> bool:
            vars: Final[list[str]] = ['name', 'card_type', 'number', 'expiration', 'cvv', 'bank', 'brand', 'slug', 'owners_name']
            return all(map(self.check_field_length, vars))

        def all_fields_present(self) -> bool:
            return bool(self.owner and self.name and (self.card_type in [slug for slug, _ in cards_types]) and self.number and self.expiration and self.cvv and (self.bank in [slug for slug, _ in cards_banks]) and (self.brand in [slug for slug, _ in cards_brands]) and self.owners_name and (self.slug == f'{self.bank}{slugify(str(self.name))}'))

        def all_fields_of_correct_types(self) -> bool:
            return [str(type(self.owner)), type(self.name), type(self.card_type), type(self.number), str(type(self.expiration)), type(self.cvv), type(self.bank), type(self.brand), type(self.slug), type(self.owners_name)] == ["<class 'account.models.User'>", str, str, str, "<class 'secret.month.Month'>", str, str, str, str, str]

        def is_valid(self) -> bool:
            if self.all_fields_present() and self.all_fields_of_correct_types() and self.all_fields_of_right_length():
                return True
            return False
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
        return f'{str(self.owner.username)} | {self.card_type} | {self.name}'
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
        return reverse('secret:card_list_view')
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
        self.name = xor(str(self.name), self.owner.password[21:])
        self.number = xor(str(self.number), self.owner.password[21:])
        self.cvv = xor(str(self.cvv), self.owner.password[21:])
        self.owners_name = xor(str(self.owners_name), self.owner.password[21:])
        self.note = xor(str(self.note), self.owner.password[21:])
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
        card: PaymentCard = super().from_db(db, field_names, values)
        card.name = xor(str(card.name), card.owner.password[21:], encrypt=False)
        card.number = xor(str(card.number), card.owner.password[21:], encrypt=False)
        card.cvv = xor(str(card.cvv), card.owner.password[21:], encrypt=False)
        card.owners_name = xor(str(card.owners_name), card.owner.password[21:], encrypt=False)
        card.note = xor(str(card.note), card.owner.password[21:], encrypt=False)
        return card
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
        max_length: Final[dict[str, int]] = {'name': 40, 'card_type': 16, 'number': 19, 'cvv': 4, 'bank': 64, 'brand': 64, 'slug': 128, 'owners_name': 64, 'note': 128}
        return max_length[var]
    ```

### `#!py def expected_min_length`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown, var: str`

Kwargs: `#!py None`

Return Type: `#!py int`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def expected_min_length(self, var: str) -> int:
        min_length: Final[dict[str, int]] = {'number': 12, 'cvv': 3}
        return min_length[var]
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
        if var == 'expiration':
            return True
        value = self.__getattribute__(var)
        if var in ['number', 'cvv']:
            return self.expected_min_length(var) <= len(value) <= self.expected_max_length(var)
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
        vars: Final[list[str]] = ['name', 'card_type', 'number', 'expiration', 'cvv', 'bank', 'brand', 'slug', 'owners_name']
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
        return bool(self.owner and self.name and (self.card_type in [slug for slug, _ in cards_types]) and self.number and self.expiration and self.cvv and (self.bank in [slug for slug, _ in cards_banks]) and (self.brand in [slug for slug, _ in cards_brands]) and self.owners_name and (self.slug == f'{self.bank}{slugify(str(self.name))}'))
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
        return [str(type(self.owner)), type(self.name), type(self.card_type), type(self.number), str(type(self.expiration)), type(self.cvv), type(self.bank), type(self.brand), type(self.slug), type(self.owners_name)] == ["<class 'account.models.User'>", str, str, str, "<class 'secret.month.Month'>", str, str, str, str, str]
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
