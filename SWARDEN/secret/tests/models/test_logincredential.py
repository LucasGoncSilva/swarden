from uuid import UUID

from CORE.testcase import create_scenarios
from account.models import User
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.test import TestCase
from django.urls import reverse

from secret.models import (
    LoginCredential,
    Service,
)


class LoginCredentialTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
        )

        self.service_1: Service = Service.objects.create(name='Service 1')
        self.service_2: Service = Service.objects.create(name='Service 2')

        # Object 1
        self.login_credential_1_pk: UUID = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_1,
            name='Personal Main Account',
            slug='service-1-personal-main-account',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        ).pk  # Correct object

        # Object 2
        self.login_credential_2_pk: UUID = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_2,
            name='Little Fries',
            slug='service-2-little-fries',
            third_party_login=True,
            third_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        ).pk  # Correct object

        # Object 3
        self.login_credential_3_pk: UUID = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_1,
            name='Little Fries',
            slug='service-1-little-fries',
            third_party_login=True,  # False or...
            third_party_login_name='-----',  # something different to '-----'
            login='night_monkey123',  # '-----'
            password='ilovemenotyou',  # '-----'
        ).pk

        # Object 4
        self.login_credential_4_pk: UUID = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_2,
            name='Little Fries',
            slug='service-2-potato',  # 'service-2-little-fries'
            third_party_login=False,
            third_party_login_name='-----',
            login='',  # Empty login
            password='night_monkey123',
        ).pk

        # Object 5
        self.login_credential_5_pk: UUID = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_1,
            name='Little Fries',
            slug='service-1-little-fries',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123',
            # Missing/empty password field
        ).pk

        # Object 6
        self.login_credential_6_pk: UUID = LoginCredential.objects.create(
            owner=self.user,
            service=self.service_2,
            name='Personal Main Account',
            slug='service-1-personal-not-main-account',  # Wrong slug
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        ).pk

    def test_credential_instance_validity(self) -> None:
        """Tests credential instance of correct class"""

        for cred in LoginCredential.objects.iterator():
            with self.subTest(cred=cred):
                self.assertIsInstance(cred, LoginCredential)

    def test_credential_key_value_assertion(self) -> None:
        """Tests credential correct attribuition of value"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1_pk
        )

        self.assertEqual(cred1.service, self.service_1)
        self.assertEqual(cred1.name, 'Personal Main Account')
        self.assertEqual(cred1.slug, 'service-1-personal-main-account')
        self.assertFalse(cred1.third_party_login)
        self.assertEqual(cred1.third_party_login_name, '-----')
        self.assertEqual(cred1.login, 'night_monkey123@gmail.com')
        self.assertEqual(cred1.password, 'ilovemenotyou')

    def test_credential_special_str_method_return(self) -> None:
        """Tests credential return value of __str__ method"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1_pk
        )

        self.assertEqual(
            cred1.__str__(),
            f'{cred1.owner.username} | {cred1.service} | {cred1.name}',
        )

    def test_credential_absolute_url_method_return(self) -> None:
        """Tests credential return value of get_absolute_url method"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1_pk
        )

        self.assertEqual(
            cred1.get_absolute_url(),
            reverse(
                'secret:credential_detail_view',
                args=('service-1-personal-main-account',),
            ),
        )

    def test_credential_user_foreign_key_validity(self) -> None:
        """Tests credential user foreign key validation"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1_pk
        )
        cred2: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_2_pk
        )

        cred1_owner: User = cred1.owner
        cred2_owner: User = cred2.owner

        self.assertEqual(cred1_owner, cred2_owner)
        self.assertEqual(cred1_owner, self.user)

    def test_credential_service_foreign_key_validity(self) -> None:
        """Tests credential service foreign key validation"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1_pk
        )

        cred1_service: Service = cred1.service

        self.assertEqual(cred1_service, self.service_1)

    def test_credential_create_validity(self) -> None:
        """Tests credential creation integrity and validation"""

        cred1: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_1_pk
        )
        cred2: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_2_pk
        )
        cred3: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_3_pk
        )
        cred4: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_4_pk
        )
        cred5: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_5_pk
        )
        cred6: LoginCredential = LoginCredential.objects.get(
            pk=self.login_credential_6_pk
        )

        self.assertEqual(LoginCredential.objects.count(), 6)

        cred1.full_clean()
        cred2.full_clean()

        with self.assertRaises(ValidationError):
            cred3.full_clean()

        with self.assertRaises(ValidationError):
            cred4.full_clean()

        with self.assertRaises(ValidationError):
            cred5.full_clean()

        with self.assertRaises(ValidationError):
            cred6.full_clean()

        with self.assertRaises(ValidationError):
            cred6.full_clean()

    def test_credential_update_validity(self) -> None:
        """Tests credential update integrity and validation"""

        LoginCredential.objects.filter(pk=self.login_credential_3_pk).update(
            third_party_login=False
        )
        LoginCredential.objects.filter(pk=self.login_credential_4_pk).update(
            slug='service-2-little-fries',
            login='some_login',
        )
        LoginCredential.objects.filter(pk=self.login_credential_5_pk).update(
            password='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        )
        LoginCredential.objects.filter(pk=self.login_credential_6_pk).update(
            slug='service-2-personal-main-account'
        )

        for cred in LoginCredential.objects.iterator():
            with self.subTest(cred=cred):
                self.assertIsNone(cred.full_clean())

    def test_credential_delete_validity(self) -> None:
        """Tests credential correct deletion"""

        for cred in LoginCredential.objects.iterator():
            with self.subTest(cred=cred):
                try:
                    cred.full_clean()
                except ValidationError:
                    cred.delete()

        self.assertEqual(LoginCredential.objects.count(), 2)

    def test_credential_db_exception_raises(self) -> None:
        """Tests credential correct integrity and validation with raised exceptions"""

        # Expecting raises
        params: list[dict[str, User | Service | str | bool]] = [
            {'owner': self.user},
            {'service': self.service_1},
            {'name': 'Name'},
            {'third_party_login': False},
            {'third_party_login_name': '-----'},
            {'login': 'LoginName'},
            {'password': 'PasswordName'},
            {'slug': 'service-1-name'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises((ValidationError, AttributeError)):
                    with atomic():
                        instance: LoginCredential = LoginCredential(**scenario)
                        instance.full_clean()

        raise_kwargs: dict[str, dict[str, User | Service | str | bool]] = {
            'cred1': {
                'owner': self.user,
                'service_id': self.service_2,
                'name': 'x' * 41,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred2': {
                'owner': self.user,
                'service_id': self.service_2,
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 41,
                'login': 'x' * 201,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred3': {
                'owner': self.user,
                'service_id': self.service_2,
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 201,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred4': {
                'owner': self.user,
                'service_id': self.service_2,
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 129,
                'slug': 'aws--' + 'x' * 123,
            },
            'cred5': {
                'owner': self.user,
                'service_id': self.service_2,
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'aws--' + 'x' * 124,
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: LoginCredential = LoginCredential(
                            **raise_kwargs[scenario]
                        )
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, User | Service | str | bool]] = {
            'cred1': {
                'owner': self.user,
                'service': self.service_2,
                'name': 'x' * 40,
                'third_party_login': False,
                'third_party_login_name': 'x' * 40,
                'login': 'x' * 200,
                'password': 'x' * 200,
                'note': 'x' * 128,
                'slug': 'service-2-' + 'x' * 40,
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: LoginCredential = LoginCredential(**no_raise_kwargs[scenario])
                instance.full_clean()
