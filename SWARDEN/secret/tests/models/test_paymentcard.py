from uuid import UUID

from CORE.testcase import create_scenarios
from account.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.transaction import atomic
from django.test import TestCase
from django.urls import reverse

from secret.models import (
    Bank,
    Brand,
    CardType,
    PaymentCard,
)
from secret.month.models import Month


class CardTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='longpassphrase',
        )

        self.card_type_1: CardType = CardType.objects.create(name='Type 1')
        self.card_type_2: CardType = CardType.objects.create(name='Type 2')

        self.bank_1: Bank = Bank.objects.create(name='Bank 1')
        self.bank_2: Bank = Bank.objects.create(name='Bank 2')

        self.brand_1: Brand = Brand.objects.create(name='Brand 1')
        self.brand_2: Brand = Brand.objects.create(name='Brand 2')

        # Object 1
        self.card_1_pk: UUID = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card One',
            owners_name='TEST USER',
            card_type=self.card_type_1,
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank=self.bank_1,
            brand=self.brand_1,
            branch='123',
            account='123',
            password='1234',
            slug='bank-1-personal-main-card-one',
        ).pk  # Correct object

        # Object 2
        self.card_2_pk: UUID = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Two',
            owners_name='TEST USER',
            card_type=self.card_type_2,
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank=self.bank_2,
            brand=self.brand_2,
            branch='456',
            account='456',
            password='5678',
            slug='bank-2-personal-main-card-two',
        ).pk  # Correct object

        # Object 3
        self.card_3_pk: UUID = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Three',
            owners_name='TEST USER',
            card_type=self.card_type_1,
            number='123456789',  # Length out of range
            expiration=Month(2028, 11),
            cvv=12,  # Length out of range
            bank=self.bank_1,
            brand=self.brand_1,
            branch='789',
            account='789',
            password='2468',
            slug='bank-1-personal-main-card-three',
        ).pk

        # Object 4
        self.card_4_pk: UUID = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card Four',
            owners_name='TEST USER',
            card_type=self.card_type_1,
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank=self.bank_1,
            brand=self.brand_1,
            branch='369',
            account='258',
            password='1011',
            slug='bank-1-personal-a-main-card-four',  # 'bank-1-personal-main-card-four'
        ).pk

    def test_card_instance_validity(self) -> None:
        """Tests card instance of correct class"""

        for card in PaymentCard.objects.iterator():
            with self.subTest(card=card):
                self.assertIsInstance(card, PaymentCard)

    def test_card_special_str_method_return(self) -> None:
        """Tests card return value of __str__ method"""

        card1: PaymentCard = PaymentCard.objects.get(pk=self.card_1_pk)

        self.assertEqual(
            card1.__str__(),
            f'{card1.owner.username} | {card1.card_type.name} | {card1.name}',
        )

    def test_card_absolute_url_method_return(self) -> None:
        """Tests card return value of get_absolute_url method"""

        cred1: PaymentCard = PaymentCard.objects.get(pk=self.card_1_pk)

        self.assertEqual(
            cred1.get_absolute_url(),
            reverse('secret:card_detail_view', args=(cred1.slug,)),
        )

    def test_card_key_value_assertion(self) -> None:
        """Tests card correct attribuition of value"""

        card1: PaymentCard = PaymentCard.objects.get(pk=self.card_1_pk)

        self.assertEqual(card1.name, 'Personal Main Card One')
        self.assertEqual(card1.card_type, self.card_type_1)
        self.assertEqual(card1.number, '4002892240028922')
        self.assertEqual(card1.expiration, Month(2028, 11))
        self.assertEqual(card1.cvv, '113')
        self.assertEqual(card1.bank, self.bank_1)
        self.assertEqual(card1.brand, self.brand_1)
        self.assertEqual(card1.branch, '123')
        self.assertEqual(card1.account, '123')
        self.assertEqual(card1.password, '1234')
        self.assertEqual(card1.slug, 'bank-1-personal-main-card-one')
        self.assertEqual(card1.owners_name, 'TEST USER')

    def test_card_user_foreign_key_validity(self) -> None:
        """Tests card user foreign key validation"""

        card1_owner: User = PaymentCard.objects.get(pk=self.card_1_pk).owner

        self.assertEqual(card1_owner, self.user)

    def test_card_create_validity(self) -> None:
        """Tests card creation integrity and validation"""

        card1: PaymentCard = PaymentCard.objects.get(pk=self.card_1_pk)
        card2: PaymentCard = PaymentCard.objects.get(pk=self.card_2_pk)
        card3: PaymentCard = PaymentCard.objects.get(pk=self.card_3_pk)
        card4: PaymentCard = PaymentCard.objects.get(pk=self.card_4_pk)

        self.assertEqual(PaymentCard.objects.count(), 4)

        card1.full_clean()
        card2.full_clean()

        with self.assertRaises(ValidationError):
            card3.full_clean()

        with self.assertRaises(ValidationError):
            card4.full_clean()

    def test_card_update_validity(self) -> None:
        """Tests card update integrity and validation"""

        PaymentCard.objects.filter(pk=self.card_3_pk).update(
            number='4002892240028922',
            cvv='762',
        )
        PaymentCard.objects.filter(pk=self.card_4_pk).update(
            bank=self.bank_2,
            slug='bank-2-personal-main-card-four',
        )

        for card in PaymentCard.objects.iterator():
            with self.subTest(card=card):
                self.assertIsNone(card.full_clean())

    def test_card_delete_validity(self) -> None:
        """Tests card correct deletion"""

        for card in PaymentCard.objects.iterator():
            with self.subTest(card=card):
                try:
                    card.full_clean()
                except ValidationError:
                    card.delete()

        self.assertEqual(PaymentCard.objects.count(), 2)

    def test_card_db_exception_raises(self) -> None:
        """Tests card correct integrity and validation with raised exceptions"""

        # Expecting raises
        params: list[dict[str, User | Bank | Brand | CardType | str]] = [
            {'owner': self.user},
            {'name': 'Name'},
            {'card_type': self.card_type_1},
            {'number': '1111222233334444'},
            {'cvv': '044'},
            {'bank': self.bank_1},
            {'brand': self.brand_1},
            {'branch': '123'},
            {'account': '123'},
            {'password': '1234'},
            {'owners_name': "Owner's Name"},
            {'slug': 'name'},
        ]

        for case, scenario in create_scenarios(params):
            with self.subTest(scenario=case):
                with self.assertRaises((ValidationError, ObjectDoesNotExist)):
                    with atomic():
                        instance: PaymentCard = PaymentCard(**scenario)
                        instance.full_clean()

        raise_kwargs: dict[
            str, dict[str, str | Month | User | Bank | Brand | CardType]
        ] = {
            'card1': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 41,
            },
            'card2': {
                'owner': self.user,
                'name': 'x' * 41,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card3': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_2,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_2.name + 'x' * 40,
            },
            'card4': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 11,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card5': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 20,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card6': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 2,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card7': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 5,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card8': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 65,
                'note': 'x' * 128,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card9': {
                'owner': self.user,
                'name': 'x' * 40,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'owners_name': 'x' * 64,
                'note': 'x' * 129,
                'slug': self.bank_1.name + 'x' * 40,
            },
            'card10': {
                'owner': self.user,
                'name': 'Name',
                'card_type': self.card_type_1,
                'number': '1111222233334444',
                'cvv': '044',
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '12',
                'account': '123',
                'password': '1234',
                'owners_name': "Owner's Name",
                'slug': 'name',
            },
            'card11': {
                'owner': self.user,
                'name': 'Name',
                'card_type': self.card_type_1,
                'number': '1111222233334444',
                'cvv': '044',
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '123456789012',
                'account': '123',
                'password': '1234',
                'owners_name': "Owner's Name",
                'slug': 'name',
            },
            'card12': {
                'owner': self.user,
                'name': 'Name',
                'card_type': self.card_type_1,
                'number': '1111222233334444',
                'cvv': '044',
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '123',
                'account': '12',
                'password': '1234',
                'owners_name': "Owner's Name",
                'slug': 'name',
            },
            'card13': {
                'owner': self.user,
                'name': 'Name',
                'card_type': self.card_type_1,
                'number': '1111222233334444',
                'cvv': '044',
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '123',
                'account': '123456789012',
                'password': '1234',
                'owners_name': "Owner's Name",
                'slug': 'name',
            },
            'card14': {
                'owner': self.user,
                'name': 'Name',
                'card_type': self.card_type_1,
                'number': '1111222233334444',
                'cvv': '044',
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '123',
                'account': '123',
                'password': '123',
                'owners_name': "Owner's Name",
                'slug': 'name',
            },
            'card15': {
                'owner': self.user,
                'name': 'Name',
                'card_type': self.card_type_1,
                'number': '1111222233334444',
                'cvv': '044',
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '123',
                'account': '123',
                'password': '1234567',
                'owners_name': "Owner's Name",
                'slug': 'name',
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: PaymentCard = PaymentCard(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[
            str, dict[str, str | Month | User | Bank | Brand | CardType]
        ] = {
            'card1': {
                'owner': self.user,
                'name': 'x' * 40,
                'owners_name': 'x' * 64,
                'card_type': self.card_type_1,
                'number': 'x' * 16,
                'expiration': Month(2044, 4),
                'cvv': 'x' * 3,
                'bank': self.bank_1,
                'brand': self.brand_1,
                'branch': '1234',
                'account': '1234',
                'password': '123456',
                'note': 'x' * 128,
                'slug': 'bank-1-' + 'x' * 40,
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: PaymentCard = PaymentCard(**no_raise_kwargs[scenario])
                instance.full_clean()
