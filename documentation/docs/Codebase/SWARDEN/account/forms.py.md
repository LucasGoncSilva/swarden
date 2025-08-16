# File: `forms.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.account`

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

### `#!py import Self`

Path: `#!py typing`

Category: native

??? example "Snippet"

    ```py
    from typing import Self
    ```

### `#!py import CaptchaField`

Path: `#!py captcha.fields`

Category: trdparty

??? example "Snippet"

    ```py
    from captcha.fields import CaptchaField
    ```

### `#!py import ReadOnlyPasswordHashField`

Path: `#!py django.contrib.auth.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.contrib.auth.forms import ReadOnlyPasswordHashField
    ```

### `#!py import CharField`

Path: `#!py django.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.forms import CharField
    ```

### `#!py import Form`

Path: `#!py django.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.forms import Form
    ```

### `#!py import ModelForm`

Path: `#!py django.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.forms import ModelForm
    ```

### `#!py import PasswordInput`

Path: `#!py django.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.forms import PasswordInput
    ```

### `#!py import TextInput`

Path: `#!py django.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.forms import TextInput
    ```

### `#!py import ValidationError`

Path: `#!py django.forms`

Category: trdparty

??? example "Snippet"

    ```py
    from django.forms import ValidationError
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

### `#!py class UserChangeForm`

Parents: `ModelForm`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class UserChangeForm(ModelForm):
        password = ReadOnlyPasswordHashField(label='Password')

        class Meta:
            model = User
            fields = ('groups', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'password', 'user_permissions', 'username')

        def clean_password(self):
            return self.initial['password']
    ```

### `#!py class UserCreationForm`

Parents: `ModelForm`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class UserCreationForm(ModelForm):
        password1: Final[CharField] = CharField(label='Password', widget=PasswordInput)
        password2: Final[CharField] = CharField(label='Password confirmation', widget=PasswordInput)

        class Meta:
            model = User
            fields: Final[tuple[str]] = ('username',)

        def clean_password2(self: Self):
            password1: str | None = self.cleaned_data.get('password1')
            password2: str | None = self.cleaned_data.get('password2')
            if password1 and password2 and (password1 != password2):
                raise ValidationError("Passwords don't match")
            return password2

        def save(self: Self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user
    ```

### `#!py class RegisterForm`

Parents: `Form`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class RegisterForm(Form):
        username: Final[CharField] = CharField(label='Username', min_length=2, max_length=20, required=True, widget=TextInput(attrs={'id': 'username', 'placeholder': 'Enter your username', 'autofocus': 'autofocus', 'autocomplete': 'off'}), help_text='Max of 20 chars. Letters, numbers and "@", ".", "+", "-", "_" only.')
        passphrase: Final[CharField] = CharField(label='Passphrase', required=True, widget=PasswordInput(attrs={'id': 'passphrase', 'placeholder': 'Enter your passphrase', 'autocomplete': 'off'}), help_text='Use a "passphase", sentence instead of random characters or just password.')
        passphrase2: Final[CharField] = CharField(label='', required=True, widget=PasswordInput(attrs={'id': 'passphrase-confirm', 'placeholder': 'Confirm your passphrase', 'autocomplete': 'off'}))
        captcha: Final[CaptchaField] = CaptchaField()
    ```

### `#!py class LogInForm`

Parents: `Form`

Decorators: `#!py None`

Kwargs: `#!py None`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    class LogInForm(Form):
        username: Final[CharField] = CharField(label='Username', min_length=2, max_length=32, required=True, widget=TextInput(attrs={'id': 'username', 'placeholder': 'Enter your username', 'autofocus': 'autofocus', 'autocomplete': 'off'}))
        passphrase: Final[CharField] = CharField(label='Passphrase', required=True, widget=PasswordInput(attrs={'id': 'passphrase', 'placeholder': 'Enter your passphrase', 'autocomplete': 'off'}))
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
        model = User
        fields = ('groups', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'password', 'user_permissions', 'username')
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
        model = User
        fields: Final[tuple[str]] = ('username',)
    ```



---

## Functions

### `#!py def clean_password`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def clean_password(self):
        return self.initial['password']
    ```

### `#!py def clean_password2`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def clean_password2(self: Self):
        password1: str | None = self.cleaned_data.get('password1')
        password2: str | None = self.cleaned_data.get('password2')
        if password1 and password2 and (password1 != password2):
            raise ValidationError("Passwords don't match")
        return password2
    ```

### `#!py def save`

Type: `#!py method`

Decorators: `#!py None`

Args: `#!py self: Self, commit: Unknown`

Kwargs: `#!py None`

Return Type: `#!py Unknown`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def save(self: Self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
