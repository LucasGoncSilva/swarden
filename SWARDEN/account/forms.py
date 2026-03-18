from typing import Final

from captcha.fields import CaptchaField
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import (
    CharField,
    Form,
    ModelForm,
    PasswordInput,
    TextInput,
    ValidationError,
)

from account.models import User


# Admin
class UserChangeForm(ModelForm):  # pragma: no cover
    password: ReadOnlyPasswordHashField = ReadOnlyPasswordHashField(label=('Password'))

    class Meta:
        model = User
        fields = (
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'password',
            'user_permissions',
            'username',
        )

    def clean_password(self):
        # Returns original password, not the new typed one
        return self.initial['password']


class UserCreationForm(ModelForm):  # pragma: no cover
    password1: Final[CharField] = CharField(label='Password', widget=PasswordInput)
    password2: Final[CharField] = CharField(
        label='Password confirmation', widget=PasswordInput
    )

    class Meta:
        model = User
        fields: Final[tuple[str]] = ('username',)

    def clean_password2(self) -> str:
        password1: str | None = self.cleaned_data.get('password1')
        password2: str | None = self.cleaned_data.get('password2')
        if not password1 or not password2 or password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


# Views
class RegisterForm(Form):
    username: Final[CharField] = CharField(
        label='Username',
        min_length=2,
        max_length=32,
        required=True,
        widget=TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Enter your username',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
            }
        ),
        help_text='Max of 20 chars. Letters, numbers and "@", ".", "+", "-", "_" only.',
    )
    passphrase: Final[CharField] = CharField(
        label='Passphrase',
        required=True,
        min_length=12,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase',
                'placeholder': 'Enter your passphrase',
                'autocomplete': 'off',
            }
        ),
        help_text='Use a "passphase", sentence (12+ chars) '
        'instead of random characters or just password.',
    )
    passphrase2: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=12,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase-confirm',
                'placeholder': 'Confirm your passphrase',
                'autocomplete': 'off',
            }
        ),
    )
    captcha: Final[CaptchaField] = CaptchaField()


class LogInForm(Form):
    username: Final[CharField] = CharField(
        label='Username',
        min_length=2,
        max_length=32,
        required=True,
        widget=TextInput(
            attrs={
                'id': 'username',
                'placeholder': 'Enter your username',
                'autofocus': 'autofocus',
                'autocomplete': 'off',
            }
        ),
    )
    passphrase: Final[CharField] = CharField(
        label='Passphrase',
        required=True,
        min_length=12,
        widget=PasswordInput(
            attrs={
                'id': 'passphrase',
                'placeholder': 'Enter your passphrase',
                'autocomplete': 'off',
            }
        ),
    )


class RecoveryTestForm(Form):
    word1: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word1',
                'placeholder': 'Word here...',
                'autocomplete': 'off',
            }
        ),
    )
    word2: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word2',
                'placeholder': 'Word here...',
                'autocomplete': 'off',
            }
        ),
    )
    word3: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word3',
                'placeholder': 'Word here...',
                'autocomplete': 'off',
            }
        ),
    )


class RecoveryWordlistForm(Form):
    word1: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word1',
                'placeholder': '1st word',
                'autocomplete': 'off',
            }
        ),
    )
    word2: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word2',
                'placeholder': '2nd word',
                'autocomplete': 'off',
            }
        ),
    )
    word3: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word3',
                'placeholder': '3rd word',
                'autocomplete': 'off',
            }
        ),
    )
    word4: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word4',
                'placeholder': '4th word',
                'autocomplete': 'off',
            }
        ),
    )
    word5: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word5',
                'placeholder': '5th word',
                'autocomplete': 'off',
            }
        ),
    )
    word6: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word6',
                'placeholder': '6th word',
                'autocomplete': 'off',
            }
        ),
    )
    word7: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word7',
                'placeholder': '7th word',
                'autocomplete': 'off',
            }
        ),
    )
    word8: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word8',
                'placeholder': '8th word',
                'autocomplete': 'off',
            }
        ),
    )
    word9: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word9',
                'placeholder': '9th word',
                'autocomplete': 'off',
            }
        ),
    )
    word10: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word10',
                'placeholder': '10th word',
                'autocomplete': 'off',
            }
        ),
    )
    word11: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word11',
                'placeholder': '11th word',
                'autocomplete': 'off',
            }
        ),
    )
    word12: Final[CharField] = CharField(
        label='',
        required=True,
        min_length=3,
        max_length=8,
        widget=TextInput(
            attrs={
                'id': 'word12',
                'placeholder': '12th word',
                'autocomplete': 'off',
            }
        ),
    )
