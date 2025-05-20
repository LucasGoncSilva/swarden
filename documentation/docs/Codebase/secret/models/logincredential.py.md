
# File: `logincredential.py`
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

### `#!py import CASCADE`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import CASCADE
    ```

### `#!py import BooleanField`

Path: `#!py django.db.models`

Category: 3rd Party

??? example "SNIPPET"

    ```py
    from django.db.models import BooleanField
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

### `#!py import credentials_services`

Path: `#!py secret.choices`

Category: Local

??? example "SNIPPET"

    ```py
    from secret.choices import credentials_services
    ```



---

## Consts

!!! info "NO CONSTANT DEFINED HERE"

---

## Classes

### `#!py class LoginCredential`

Parents: `Model`

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class LoginCredential(Model):
        id: Final[UUIDField] = UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
        owner: Final[ForeignKey] = ForeignKey(User, on_delete=CASCADE, related_name='credentials', verbose_name='Dono')
        service: CharField = CharField(max_length=64, choices=credentials_services, verbose_name='Serviço', validators=[MaxLengthValidator(64)])
        name: CharField = CharField(max_length=40, verbose_name='Apelido (ex: Conta Principal)', validators=[MaxLengthValidator(40)])
        third_party_login: BooleanField = BooleanField(verbose_name='Login com serviço de terceiro?')
        third_party_login_name: CharField = CharField(max_length=40, verbose_name='Apelido do serviço de terceiro', validators=[MaxLengthValidator(40)])
        login: CharField = CharField(max_length=200, verbose_name='Login', validators=[MaxLengthValidator(200)])
        password: CharField = CharField(max_length=200, verbose_name='Senha', validators=[MaxLengthValidator(200)])
        note: TextField = TextField(max_length=128, blank=True, null=True, verbose_name='Anotação particular', validators=[MaxLengthValidator(128)])
        slug: Final[SlugField] = SlugField(max_length=128, validators=[MaxLengthValidator(128)])
        created: Final[DateTimeField] = DateTimeField(auto_now_add=True, verbose_name='Criado em')
        updated: Final[DateTimeField] = DateTimeField(auto_now=True, verbose_name='Atualizado em')

        class Meta:
            ordering: Final[list[str]] = ['-created']
            verbose_name: Final[str] = 'Credencial'
            verbose_name_plural: Final[str] = 'Credenciais'

        def __str__(self) -> str:
            return f'{str(self.owner.username)} | {self.service} | {self.name}'

        def get_absolute_url(self) -> str:
            return reverse('secret:credential_list_view')

        def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
            self.third_party_login_name = xor(str(self.third_party_login_name), self.owner.password[21:])
            self.login = xor(str(self.login), self.owner.password[21:])
            self.password = xor(str(self.password), self.owner.password[21:])
            self.note = xor(str(self.note), self.owner.password[21:])
            return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

        @classmethod
        def from_db(cls, db, field_names, values):
            cred: LoginCredential = super().from_db(db, field_names, values)
            cred.third_party_login_name = xor(str(cred.third_party_login_name), cred.owner.password[21:], encrypt=False)
            cred.login = xor(str(cred.login), cred.owner.password[21:], encrypt=False)
            cred.password = xor(str(cred.password), cred.owner.password[21:], encrypt=False)
            cred.note = xor(str(cred.note), cred.owner.password[21:], encrypt=False)
            return cred

        def expected_max_length(self, var: str) -> int:
            max_length: Final[dict[str, int]] = {'service': 64, 'name': 40, 'slug': 128, 'third_party_login_name': 40, 'login': 200, 'password': 200}
            return max_length[var]

        def check_field_length(self, var: str) -> bool:
            value = self.__getattribute__(var)
            return len(value) <= self.expected_max_length(var)

        def all_fields_of_right_length(self) -> bool:
            vars: Final[list[str]] = ['service', 'name', 'slug', 'third_party_login_name', 'login', 'password']
            return all(map(self.check_field_length, vars))

        def all_fields_present(self) -> bool:
            if self.owner and self.name and (self.service in [slug for (slug, _) in credentials_services]) and (self.slug == f'{self.service}{slugify(str(self.name))}') and self.third_party_login_name and self.login and self.password:
                if self.third_party_login and self.third_party_login_name != '-----' or (not self.third_party_login and self.login != '-----' and (self.password != '-----')):
                    return True
            return False

        def all_fields_of_correct_types(self) -> bool:
            return [str(type(self.owner)), type(self.service), type(self.name), type(self.slug), type(self.third_party_login), type(self.third_party_login_name), type(self.login), type(self.password)] == ["<class 'account.models.User'>", str, str, str, bool, str, str, str]

        def is_valid(self) -> bool:
            if self.all_fields_present() and self.all_fields_of_correct_types() and self.all_fields_of_right_length():
                return True
            return False
    ```

### `#!py class Meta`

Parents: ``

Decorators: `#!py None`

Kwargs: `#!py None`

??? example "SNIPPET"

    ```py
    class Meta:
        ordering: Final[list[str]] = ['-created']
        verbose_name: Final[str] = 'Credencial'
        verbose_name_plural: Final[str] = 'Credenciais'
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
        return f'{str(self.owner.username)} | {self.service} | {self.name}'
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
        return reverse('secret:credential_list_view')
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
        self.third_party_login_name = xor(str(self.third_party_login_name), self.owner.password[21:])
        self.login = xor(str(self.login), self.owner.password[21:])
        self.password = xor(str(self.password), self.owner.password[21:])
        self.note = xor(str(self.note), self.owner.password[21:])
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
        cred: LoginCredential = super().from_db(db, field_names, values)
        cred.third_party_login_name = xor(str(cred.third_party_login_name), cred.owner.password[21:], encrypt=False)
        cred.login = xor(str(cred.login), cred.owner.password[21:], encrypt=False)
        cred.password = xor(str(cred.password), cred.owner.password[21:], encrypt=False)
        cred.note = xor(str(cred.note), cred.owner.password[21:], encrypt=False)
        return cred
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
        max_length: Final[dict[str, int]] = {'service': 64, 'name': 40, 'slug': 128, 'third_party_login_name': 40, 'login': 200, 'password': 200}
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
        vars: Final[list[str]] = ['service', 'name', 'slug', 'third_party_login_name', 'login', 'password']
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
        if self.owner and self.name and (self.service in [slug for (slug, _) in credentials_services]) and (self.slug == f'{self.service}{slugify(str(self.name))}') and self.third_party_login_name and self.login and self.password:
            if self.third_party_login and self.third_party_login_name != '-----' or (not self.third_party_login and self.login != '-----' and (self.password != '-----')):
                return True
        return False
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
        return [str(type(self.owner)), type(self.service), type(self.name), type(self.slug), type(self.third_party_login), type(self.third_party_login_name), type(self.login), type(self.password)] == ["<class 'account.models.User'>", str, str, str, bool, str, str, str]
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
