from uuid import UUID

from django.test import TestCase

from secret.models import CardType


class CardTypeTestCase(TestCase):
    def setUp(self) -> None:
        self.card_type_1_pk: UUID = CardType.objects.create(name='CardType 1').pk

        self.card_type_2_pk: UUID = CardType.objects.create(name='CardType 2').pk

        self.card_type_3_pk: UUID = CardType.objects.create(name='CardType 3').pk

        self.card_type_4_pk: UUID = CardType.objects.create(name='CardType 4').pk

        self.card_type_5_pk: UUID = CardType.objects.create(name='CardType 5').pk

    def test_card_type_instance_validity(self) -> None:
        """Tests card_type instance of correct class"""

        for card_type in CardType.objects.iterator():
            with self.subTest(card_type=card_type):
                self.assertIsInstance(card_type, CardType)

    def test_card_type_special_str_method_return(self) -> None:
        """Tests card_type return value of __str__ method"""

        card_type: CardType = CardType.objects.get(pk=self.card_type_1_pk)

        self.assertEqual(card_type.__str__(), 'CardType 1')

    def test_card_type_key_value_assertion(self) -> None:
        """Tests card_type correct attribuition of value"""

        card_type1: CardType = CardType.objects.get(pk=self.card_type_1_pk)

        self.assertEqual(card_type1.name, 'CardType 1')

    def test_card_type_create_validity(self) -> None:
        """Tests card_type creation integrity and validation"""

        card_type1: CardType = CardType.objects.get(pk=self.card_type_1_pk)
        card_type2: CardType = CardType.objects.get(pk=self.card_type_2_pk)
        card_type3: CardType = CardType.objects.get(pk=self.card_type_3_pk)
        card_type4: CardType = CardType.objects.get(pk=self.card_type_4_pk)
        card_type5: CardType = CardType.objects.get(pk=self.card_type_5_pk)

        self.assertEqual(CardType.objects.count(), 5)

        self.assertIsNone(card_type1.full_clean())
        self.assertIsNone(card_type2.full_clean())
        self.assertIsNone(card_type3.full_clean())
        self.assertIsNone(card_type4.full_clean())
        self.assertIsNone(card_type5.full_clean())

    def test_card_type_update_validity(self) -> None:
        """Tests card_type update integrity and validation"""

        CardType.objects.filter(pk=self.card_type_4_pk).update(
            name='CardType 4 Updated'
        )

        CardType.objects.filter(pk=self.card_type_5_pk).update(
            name='CardType 5 Updated'
        )

        for card_type in CardType.objects.iterator():
            with self.subTest(card_type=card_type):
                self.assertIsNone(card_type.full_clean())
