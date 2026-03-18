from uuid import UUID

from django.test import TestCase

from secret.models import Bank


class BankTestCase(TestCase):
    def setUp(self) -> None:
        self.bank_1_pk: UUID = Bank.objects.create(name='Bank 1').pk

        self.bank_2_pk: UUID = Bank.objects.create(name='Bank 2').pk

        self.bank_3_pk: UUID = Bank.objects.create(name='Bank 3').pk

        self.bank_4_pk: UUID = Bank.objects.create(name='Bank 4').pk

        self.bank_5_pk: UUID = Bank.objects.create(name='Bank 5').pk

    def test_bank_instance_validity(self) -> None:
        """Tests bank instance of correct class"""

        for bank in Bank.objects.iterator():
            with self.subTest(bank=bank):
                self.assertIsInstance(bank, Bank)

    def test_bank_special_str_method_return(self) -> None:
        """Tests bank return value of __str__ method"""

        bank: Bank = Bank.objects.get(pk=self.bank_1_pk)

        self.assertEqual(bank.__str__(), 'Bank 1')

    def test_bank_key_value_assertion(self) -> None:
        """Tests bank correct attribuition of value"""

        bank1: Bank = Bank.objects.get(pk=self.bank_1_pk)

        self.assertEqual(bank1.name, 'Bank 1')

    def test_bank_create_validity(self) -> None:
        """Tests bank creation integrity and validation"""

        bank1: Bank = Bank.objects.get(pk=self.bank_1_pk)
        bank2: Bank = Bank.objects.get(pk=self.bank_2_pk)
        bank3: Bank = Bank.objects.get(pk=self.bank_3_pk)
        bank4: Bank = Bank.objects.get(pk=self.bank_4_pk)
        bank5: Bank = Bank.objects.get(pk=self.bank_5_pk)

        self.assertEqual(Bank.objects.count(), 5)

        self.assertIsNone(bank1.full_clean())
        self.assertIsNone(bank2.full_clean())
        self.assertIsNone(bank3.full_clean())
        self.assertIsNone(bank4.full_clean())
        self.assertIsNone(bank5.full_clean())

    def test_bank_update_validity(self) -> None:
        """Tests bank update integrity and validation"""

        Bank.objects.filter(pk=self.bank_4_pk).update(name='Bank 4 Updated')

        Bank.objects.filter(pk=self.bank_5_pk).update(name='Bank 5 Updated')

        for bank in Bank.objects.iterator():
            with self.subTest(bank=bank):
                self.assertIsNone(bank.full_clean())
