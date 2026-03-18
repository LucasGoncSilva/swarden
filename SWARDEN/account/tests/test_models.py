from datetime import datetime
from uuid import UUID
from warnings import filterwarnings

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.test import TestCase

from account.models import ActivationAccountToken, RecoveryPhrase, User


class ActivationAccountTokenTestCase(TestCase):
    def setUp(self) -> None:
        filterwarnings('ignore', category=RuntimeWarning)

        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
        )

        self.token_1_pk: UUID = ActivationAccountToken.objects.create(
            value='x' * 64, user=self.user, used=False
        ).pk

        self.token_2_pk: UUID = ActivationAccountToken.objects.create(
            value='x' * 64, user=self.user, used=True
        ).pk

        self.token_3_pk: UUID = ActivationAccountToken.objects.create(
            value='x' * 64, user=self.user, used=False, created=None
        ).pk

        self.token_4_pk: UUID = ActivationAccountToken.objects.create(
            value=int, user=self.user, used=False
        ).pk

        self.token_5_pk: UUID = ActivationAccountToken.objects.create(
            value='x' * 63, user=self.user, used=False
        ).pk

    def test_token_instance_validity(self) -> None:
        """Tests token instance of correct class"""

        for token in ActivationAccountToken.objects.iterator():
            with self.subTest(token=token):
                self.assertIsInstance(token, ActivationAccountToken)

    def test_token_special_str_method_return(self) -> None:
        """Tests token return value of __str__ method"""

        token_1: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_1_pk
        )

        self.assertEqual(token_1.__str__(), 'x' * 64)

    def test_token_key_value_assertion(self) -> None:
        """Tests token correct attribuition of value"""

        token_1: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_1_pk
        )

        self.assertEqual(token_1.value, 'x' * 64)
        self.assertFalse(token_1.used)
        self.assertIsInstance(token_1.created, datetime)

    def test_token_create_validity(self) -> None:
        """Tests token creation integrity and validation"""

        token_1: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_1_pk
        )
        token_2: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_2_pk
        )
        token_3: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_3_pk
        )
        token_4: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_4_pk
        )
        token_5: ActivationAccountToken = ActivationAccountToken.objects.get(
            pk=self.token_5_pk
        )

        self.assertEqual(ActivationAccountToken.objects.count(), 5)

        token_1.full_clean()
        token_2.full_clean()
        token_3.full_clean()

        with self.assertRaises(ValidationError):
            token_4.full_clean()

        with self.assertRaises(ValidationError):
            token_5.full_clean()

    def test_token_update_validity(self) -> None:
        """Tests token update integrity and validation"""

        ActivationAccountToken.objects.filter(pk=self.token_4_pk).update(
            value='x' * 64, created='2009-6-5'
        )

        ActivationAccountToken.objects.filter(pk=self.token_5_pk).update(
            value='x' * 64, used=True
        )

        for token in ActivationAccountToken.objects.iterator():
            with self.subTest(token=token):
                self.assertIsNone(token.full_clean())

    def test_token_delete_validity(self) -> None:
        """Tests token correct deletion"""

        for token in ActivationAccountToken.objects.iterator():
            try:
                token.full_clean()
            except ValidationError:
                token.delete()

        self.assertEqual(ActivationAccountToken.objects.count(), 3)

    def test_token_db_exception_raises(self) -> None:
        """Tests token correct integrity and validation with raised exceptions"""

        # Expecting raises
        raise_kwargs: dict[str, dict[str, str | bool | int | None]] = {
            'token_1': {'value': 'x' * 63},
            'token2': {'value': 'x' * 65},
            'token3': {'used': True},
            'token4': {'used': False},
            'token5': {'value': 'x' * 64, 'used': None},
            'token6': {'value': 'x' * 64, 'used': 'foo'},
            'token7': {'value': 'x' * 64, 'used': 2},
            'token8': {'value': 'x' * 64},
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance = ActivationAccountToken(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, str | User | bool | datetime]] = {
            'token_1': {'value': 'x' * 64, 'user': self.user},
            'token2': {'value': 'x' * 64, 'user': self.user, 'used': False},
            'token3': {'value': 'x' * 64, 'user': self.user, 'used': True},
            'token4': {
                'value': 'x' * 64,
                'user': self.user,
                'created': datetime(2004, 5, 25),
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: ActivationAccountToken = ActivationAccountToken(
                    **no_raise_kwargs[scenario]
                )
                instance.full_clean()


class RecoveryPhraseTestCase(TestCase):
    def setUp(self) -> None:
        filterwarnings('ignore', category=RuntimeWarning)

        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
        )

        self.recovery_phrase_1_pk: UUID = RecoveryPhrase.objects.create(
            user=self.user,
            phrase_hash=make_password('phrase1'),
            fingerprint='x' * 64,
            is_active=True,
        ).pk  # Correct Object

        self.recovery_phrase_2_pk: UUID = RecoveryPhrase.objects.create(
            user=User.objects.create_user(
                username='username2', password='longpassphrase'
            ),
            phrase_hash=make_password('phrase2'),
            fingerprint='y' * 64,
            is_active=False,
        ).pk  # Correct Object

        self.recovery_phrase_3_pk: UUID = RecoveryPhrase.objects.create(
            user=User.objects.create_user(
                username='username3', password='longpassphrase'
            ),
            phrase_hash=make_password('phrase3'),
            fingerprint='z' * 64,
            is_active=False,
        ).pk  # Correct Object

        self.recovery_phrase_4_pk: UUID = RecoveryPhrase.objects.create(
            user=User.objects.create_user(
                username='username4', password='longpassphrase'
            ),
            phrase_hash=int,
            fingerprint='a' * 64,
            is_active=False,
        ).pk

        self.recovery_phrase_5_pk: UUID = RecoveryPhrase.objects.create(
            user=User.objects.create_user(
                username='username5', password='longpassphrase'
            ),
            phrase_hash=make_password('phrase5'),
            fingerprint='x' * 63,
            is_active=True,
            created=datetime,
        ).pk

    def test_recovery_phrase_instance_validity(self) -> None:
        """Tests recovery_phrase instance of correct class"""

        for recovery_phrase in RecoveryPhrase.objects.iterator():
            with self.subTest(recovery_phrase=recovery_phrase):
                self.assertIsInstance(recovery_phrase, RecoveryPhrase)

    def test_recovery_phrase_special_str_method_return(self) -> None:
        """Tests recovery_phrase return value of __str__ method"""

        recovery_phrase_1: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_1_pk
        )

        self.assertEqual(
            recovery_phrase_1.__str__(), f'{self.user.username} | {"x" * 64}'
        )

    def test_recovery_phrase_key_value_assertion(self) -> None:
        """Tests recovery_phrase correct attribuition of value"""

        recovery_phrase_1: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_1_pk
        )

        self.assertTrue(recovery_phrase_1.is_valid_phrase('phrase1'))
        self.assertEqual(recovery_phrase_1.fingerprint, 'x' * 64)
        self.assertTrue(recovery_phrase_1.is_active)
        self.assertIsInstance(recovery_phrase_1.created, datetime)

    def test_recovery_phrase_create_validity(self) -> None:
        """Tests recovery_phrase creation integrity and validation"""

        recovery_phrase_1: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_1_pk
        )
        recovery_phrase_2: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_2_pk
        )
        recovery_phrase_3: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_3_pk
        )
        recovery_phrase_4: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_4_pk
        )
        recovery_phrase_5: RecoveryPhrase = RecoveryPhrase.objects.get(
            pk=self.recovery_phrase_5_pk
        )

        self.assertEqual(RecoveryPhrase.objects.count(), 5)

        recovery_phrase_1.full_clean()
        recovery_phrase_2.full_clean()
        recovery_phrase_3.full_clean()

        with self.assertRaises(ValidationError):
            recovery_phrase_4.full_clean()

        with self.assertRaises(ValidationError):
            recovery_phrase_5.full_clean()

    def test_recovery_phrase_update_validity(self) -> None:
        """Tests recovery_phrase update integrity and validation"""

        RecoveryPhrase.objects.filter(pk=self.recovery_phrase_4_pk).update(
            phrase_hash=make_password('b' * 64), created='2009-6-5'
        )

        RecoveryPhrase.objects.filter(pk=self.recovery_phrase_5_pk).update(
            fingerprint='c' * 64, created=datetime(2026, 1, 1)
        )

        for recovery_phrase in RecoveryPhrase.objects.iterator():
            with self.subTest(recovery_phrase=recovery_phrase):
                self.assertIsNone(recovery_phrase.full_clean())

    def test_recovery_phrase_delete_validity(self) -> None:
        """Tests recovery_phrase correct deletion"""

        for recovery_phrase in RecoveryPhrase.objects.iterator():
            try:
                recovery_phrase.full_clean()
            except ValidationError:
                recovery_phrase.delete()

        self.assertEqual(RecoveryPhrase.objects.count(), 3)

    def test_recovery_phrase_db_exception_raises(self) -> None:
        """Tests recovery_phrase integrity and validation with raised exceptions"""

        # Expecting raises
        raise_kwargs: dict[str, dict[str, str | bool | int | None | User]] = {
            'recovery_phrase_1': {
                'user': User.objects.create_user(
                    username='anotheruser', password='longpassphrase'
                )
            },
            'recovery_phrase2': {'user': self.user},
            'recovery_phrase3': {'phrase_hash': make_password('gimmegimmegimme')},
            'recovery_phrase4': {'fingerprint': 'x' * 64},
            'recovery_phrase5': {'is_active': True},
            'recovery_phrase6': {'is_active': 'False'},
            'recovery_phrase7': {
                'user': User.objects.create_user(
                    username='anotheruser2', password='longpassphrase'
                ),
                'phrase_hash': make_password('gimmegimmegimme'),
            },
            'recovery_phrase8': {
                'user': User.objects.create_user(
                    username='anotheruser3', password='longpassphrase'
                ),
                'fingerprint': 'x' * 64,
            },
            'recovery_phrase9': {
                'user': User.objects.create_user(
                    username='anotheruser4', password='longpassphrase'
                ),
                'is_active': True,
            },
            'recovery_phrase_10': {
                'phrase_hash': make_password('gimmegimmegimme'),
                'fingerprint': 'x' * 64,
            },
            'recovery_phrase_11': {
                'phrase_hash': make_password('gimmegimmegimme'),
                'is_active': True,
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance = RecoveryPhrase(**raise_kwargs[scenario])
                        instance.full_clean()

    def test_recovery_phrase_duplicity(self) -> None:
        """Tests recovery_phrase exception for creating RecoveryPhrase in duplicity"""

        with self.assertRaisesMessage(
            PermissionError, 'This user already have a 12-words recovery list.'
        ):
            RecoveryPhrase.create_user_recovery(self.user)
