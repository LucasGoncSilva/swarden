from typing import NamedTuple

from captcha.models import CaptchaStore
from django.test import TestCase

from account.forms import (
    LogInForm,
    RecoveryTestForm,
    RecoveryWordlistForm,
    RegisterForm,
)


class MinMaxLen(NamedTuple):
    min_len: int
    max_len: int


class RegisterFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.FIELD_MIN_MAX_LENGTHS: dict[str, MinMaxLen] = {
            'username': MinMaxLen(min_len=2, max_len=32),
            'passphrase': MinMaxLen(min_len=12, max_len=-1),
            'passphrase2': MinMaxLen(min_len=12, max_len=-1),
        }

    def setUp(self) -> None:
        self.captcha_response = 'PASSED'
        self.valid_payload: dict[str, str] = {
            'username': 'username',
            'passphrase': 'longpassphrase',
            'passphrase2': 'longpassphrase',
            'captcha_0': CaptchaStore.generate_key(),
            'captcha_1': 'PASSED',
        }

    def test_register_form_valid_data(self) -> None:
        """Valid form"""

        form: RegisterForm = RegisterForm(data=self.valid_payload)

        self.assertTrue(form.is_valid())

    def test_register_form_no_required(self) -> None:
        """Required fields"""

        for i in self.valid_payload:
            with self.subTest(input=i):
                data: dict[str, str] = self.valid_payload.copy()
                del data[i]

                form: RegisterForm = RegisterForm(data=data)

                self.assertFalse(form.is_valid())

                if 'captcha' in i:
                    self.assertIn('captcha', form.errors)
                    self.assertEqual(
                        form.errors['captcha'], ['This field is required.']
                    )
                else:
                    self.assertIn(i, form.errors)
                    self.assertEqual(form.errors[i], ['This field is required.'])

    def test_register_form_less_than_min_length(self) -> None:
        """Min length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.min_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected - 1)

                form: RegisterForm = RegisterForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at least {expected} characters '
                        f'(it has {expected - 1}).'
                    ],
                )

    def test_register_form_more_than_max_length(self) -> None:
        """Max length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.max_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected + 1)

                form: RegisterForm = RegisterForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at most {expected} characters '
                        f'(it has {expected + 1}).'
                    ],
                )


class LogInFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.FIELD_MIN_MAX_LENGTHS: dict[str, MinMaxLen] = {
            'username': MinMaxLen(min_len=2, max_len=32),
            'passphrase': MinMaxLen(min_len=12, max_len=-1),
        }

    def setUp(self) -> None:
        self.valid_payload: dict[str, str] = {
            'username': 'username',
            'passphrase': 'longpassphrase',
        }

    def test_login_form_valid_data(self) -> None:
        """Valid form"""

        form: LogInForm = LogInForm(data=self.valid_payload)

        self.assertTrue(form.is_valid())

    def test_login_form_no_required(self) -> None:
        """Required fields"""

        for i in self.valid_payload:
            with self.subTest(input=i):
                data: dict[str, str] = self.valid_payload.copy()
                del data[i]

                form: LogInForm = LogInForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(i, form.errors)
                self.assertEqual(form.errors[i], ['This field is required.'])

    def test_login_form_less_than_min_length(self) -> None:
        """Min length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.min_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected - 1)

                form: LogInForm = LogInForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at least {expected} characters '
                        f'(it has {expected - 1}).'
                    ],
                )

    def test_login_form_more_than_max_length(self) -> None:
        """Max length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.max_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected + 1)

                form: LogInForm = LogInForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at most {expected} characters '
                        f'(it has {expected + 1}).'
                    ],
                )


class RecoveryTestFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.FIELD_MIN_MAX_LENGTHS: dict[str, MinMaxLen] = {
            'word1': MinMaxLen(min_len=3, max_len=8),
            'word2': MinMaxLen(min_len=3, max_len=8),
            'word3': MinMaxLen(min_len=3, max_len=8),
        }

    def setUp(self) -> None:
        self.valid_payload: dict[str, str] = {
            'word1': 'first',
            'word2': 'second',
            'word3': 'third',
        }

    def test_recovery_test_form_valid_data(self) -> None:
        """Valid form"""

        form: RecoveryTestForm = RecoveryTestForm(data=self.valid_payload)

        self.assertTrue(form.is_valid())

    def test_recovery_test_form_no_required(self) -> None:
        """Required fields"""

        for i in self.valid_payload:
            with self.subTest(input=i):
                data: dict[str, str] = self.valid_payload.copy()
                del data[i]

                form: RecoveryTestForm = RecoveryTestForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(i, form.errors)
                self.assertEqual(form.errors[i], ['This field is required.'])

    def test_recovery_test_form_less_than_min_length(self) -> None:
        """Min length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.min_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected - 1)

                form: RecoveryTestForm = RecoveryTestForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at least {expected} characters '
                        f'(it has {expected - 1}).'
                    ],
                )

    def test_recovery_test_form_more_than_max_length(self) -> None:
        """Max length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.max_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected + 1)

                form: RecoveryTestForm = RecoveryTestForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at most {expected} characters '
                        f'(it has {expected + 1}).'
                    ],
                )


class RecoveryWordlistFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.FIELD_MIN_MAX_LENGTHS: dict[str, MinMaxLen] = {
            'word1': MinMaxLen(min_len=3, max_len=8),
            'word2': MinMaxLen(min_len=3, max_len=8),
            'word3': MinMaxLen(min_len=3, max_len=8),
            'word4': MinMaxLen(min_len=3, max_len=8),
            'word5': MinMaxLen(min_len=3, max_len=8),
            'word6': MinMaxLen(min_len=3, max_len=8),
            'word7': MinMaxLen(min_len=3, max_len=8),
            'word8': MinMaxLen(min_len=3, max_len=8),
            'word9': MinMaxLen(min_len=3, max_len=8),
            'word10': MinMaxLen(min_len=3, max_len=8),
            'word11': MinMaxLen(min_len=3, max_len=8),
            'word12': MinMaxLen(min_len=3, max_len=8),
        }

    def setUp(self) -> None:
        self.valid_payload: dict[str, str] = {
            'word1': 'first',
            'word2': 'second',
            'word3': 'third',
            'word4': 'fourth',
            'word5': 'fifth',
            'word6': 'sixth',
            'word7': 'seventh',
            'word8': 'eighth',
            'word9': 'nineth',
            'word10': 'tenth',
            'word11': 'eleventh',
            'word12': 'twelfth',
        }

    def test_recovery_wordlist_form_valid_data(self) -> None:
        """Valid form"""

        form: RecoveryWordlistForm = RecoveryWordlistForm(data=self.valid_payload)

        self.assertTrue(form.is_valid())

    def test_recovery_wordlist_form_no_required(self) -> None:
        """Required fields"""

        for i in self.valid_payload:
            with self.subTest(input=i):
                data: dict[str, str] = self.valid_payload.copy()
                del data[i]

                form: RecoveryWordlistForm = RecoveryWordlistForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(i, form.errors)
                self.assertEqual(form.errors[i], ['This field is required.'])

    def test_recovery_wordlist_form_less_than_min_length(self) -> None:
        """Min length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.min_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected - 1)

                form: RecoveryWordlistForm = RecoveryWordlistForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at least {expected} characters '
                        f'(it has {expected - 1}).'
                    ],
                )

    def test_recovery_wordlist_form_more_than_max_length(self) -> None:
        """Max length validation"""

        for k, v in self.FIELD_MIN_MAX_LENGTHS.items():
            with self.subTest(input=k):
                data: dict[str, str] = self.valid_payload.copy()

                expected: int = v.max_len

                if expected == -1:  # pragma: no cover
                    continue

                data[k] = 'w' * (expected + 1)

                form: RecoveryWordlistForm = RecoveryWordlistForm(data=data)

                self.assertFalse(form.is_valid())
                self.assertIn(k, form.errors)
                self.assertEqual(
                    form.errors[k],
                    [
                        f'Ensure this value has at most {expected} characters '
                        f'(it has {expected + 1}).'
                    ],
                )
