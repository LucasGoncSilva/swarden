from warnings import filterwarnings
from datetime import datetime

from django.db import DataError, IntegrityError
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.test import TestCase

from account.models import ActivationAccountToken


class ActivationAccountTokenTestCase(TestCase):
    def setUp(self) -> None:
        filterwarnings("ignore", category=RuntimeWarning)

        self.token1 = ActivationAccountToken.objects.create(value='x' * 64, used=False)

        self.token2 = ActivationAccountToken.objects.create(value='x' * 64, used=True)

        self.token3 = ActivationAccountToken.objects.create(
            value='x' * 64, used=False, created=None
        )

        try:
            with atomic():
                self.token4 = ActivationAccountToken.objects.create(
                    value='x' * 65, used=False
                )
        except DataError:
            self.token4 = ActivationAccountToken.objects.create(value=int, used=False)

        self.token5 = ActivationAccountToken.objects.create(value='x' * 63, used=False)

    def test_token_instance_validity(self) -> None:
        """Tests model instance of correct class"""

        for i, token in enumerate(ActivationAccountToken.objects.all()):
            with self.subTest(token=i + 1):
                self.assertIsInstance(token, ActivationAccountToken)

    def test_token_key_value_assertion(self) -> None:
        """Tests model correct attribuition of value"""

        token1 = ActivationAccountToken.objects.get(pk=self.token1.pk)

        self.assertEqual(token1.value, 'x' * 64)
        self.assertFalse(token1.used)
        self.assertIsInstance(token1.created, datetime)

    def test_token_create_validity(self) -> None:
        """Tests model creation integrity and validation"""

        token1 = ActivationAccountToken.objects.get(pk=self.token1.pk)
        token2 = ActivationAccountToken.objects.get(pk=self.token2.pk)
        token3 = ActivationAccountToken.objects.get(pk=self.token3.pk)
        token4 = ActivationAccountToken.objects.get(pk=self.token4.pk)
        token5 = ActivationAccountToken.objects.get(pk=self.token5.pk)

        self.assertEqual(ActivationAccountToken.objects.all().count(), 5)

        self.assertTrue(token1.is_valid())
        self.assertTrue(token2.is_valid())
        self.assertTrue(token3.is_valid())
        self.assertFalse(token4.is_valid())
        self.assertFalse(token5.is_valid())

    def test_token_update_validity(self) -> None:
        """Tests model update integrity and validation"""

        ActivationAccountToken.objects.filter(pk=self.token4.pk).update(
            value='x' * 64, created='2009-6-5'
        )

        ActivationAccountToken.objects.filter(pk=self.token5.pk).update(
            value='x' * 64, used=True
        )

        for i, token in enumerate(ActivationAccountToken.objects.all()):
            with self.subTest(token=i + 1):
                self.assertTrue(token.is_valid())

    def test_token_delete_validity(self) -> None:
        """Tests model correct deletion"""

        for token in ActivationAccountToken.objects.all():
            if not token.is_valid():
                token.delete()

        self.assertEqual(ActivationAccountToken.objects.all().count(), 3)

    def test_token_db_exception_raises(self) -> None:
        """Tests model correct integrity and validation with raised exceptions"""

        # Expecting raises
        raise_kwargs: dict[str, dict[str, str | bool | int | None]] = {
            'token1': {'value': 'x' * 63},
            'token2': {'value': 'x' * 65},
            'token3': {'used': True},
            'token4': {'used': False},
            'token5': {'value': 'x' * 64, 'used': None},
            'token6': {'value': 'x' * 64, 'used': 'foo'},
            'token7': {'value': 'x' * 64, 'used': 2},
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance = ActivationAccountToken(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        try:
            no_raise_kwargs: dict[str, dict[str, str | bool | datetime]] = {
                'token1': {'value': 'x' * 64},
                'token2': {'value': 'x' * 64, 'used': False},
                'token3': {'value': 'x' * 64, 'used': True},
                'token4': {'value': 'x' * 64, 'created': datetime(2004, 5, 25)},
            }

            for scenario in no_raise_kwargs.keys():
                with self.subTest(scenario=scenario):
                    instance = ActivationAccountToken(**no_raise_kwargs[scenario])
                    instance.full_clean()

        except Exception as e:
            self.fail(
                f'ActivationAccountToken({scenario}) raised unexpected exception: {e}'
            )