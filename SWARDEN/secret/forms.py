from typing import Any

from django.forms import ModelForm

from secret.models import LoginCredential, PaymentCard, SecurityNote


class LoginCredentialForm(ModelForm):
    class Meta:
        model: type = LoginCredential
        exclude: tuple[str, ...] = ('owner',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'autocomplete': 'off'})


class PaymentCardForm(ModelForm):
    class Meta:
        model: type = PaymentCard
        exclude: tuple[str, ...] = ('owner',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'autocomplete': 'off'})


class SecurityNoteForm(ModelForm):
    class Meta:
        model: type = SecurityNote
        exclude: tuple[str, ...] = ('owner',)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'autocomplete': 'off'})
