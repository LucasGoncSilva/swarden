from uuid import UUID

from django.test import TestCase

from secret.models import Brand


class BrandTestCase(TestCase):
    def setUp(self) -> None:
        self.brand_1_pk: UUID = Brand.objects.create(name='Brand 1').pk

        self.brand_2_pk: UUID = Brand.objects.create(name='Brand 2').pk

        self.brand_3_pk: UUID = Brand.objects.create(name='Brand 3').pk

        self.brand_4_pk: UUID = Brand.objects.create(name='Brand 4').pk

        self.brand_5_pk: UUID = Brand.objects.create(name='Brand 5').pk

    def test_brand_instance_validity(self) -> None:
        """Tests brand instance of correct class"""

        for brand in Brand.objects.iterator():
            with self.subTest(brand=brand):
                self.assertIsInstance(brand, Brand)

    def test_brand_special_str_method_return(self) -> None:
        """Tests brand return value of __str__ method"""

        brand: Brand = Brand.objects.get(pk=self.brand_1_pk)

        self.assertEqual(brand.__str__(), 'Brand 1')

    def test_brand_key_value_assertion(self) -> None:
        """Tests brand correct attribuition of value"""

        brand1: Brand = Brand.objects.get(pk=self.brand_1_pk)

        self.assertEqual(brand1.name, 'Brand 1')

    def test_brand_create_validity(self) -> None:
        """Tests brand creation integrity and validation"""

        brand1: Brand = Brand.objects.get(pk=self.brand_1_pk)
        brand2: Brand = Brand.objects.get(pk=self.brand_2_pk)
        brand3: Brand = Brand.objects.get(pk=self.brand_3_pk)
        brand4: Brand = Brand.objects.get(pk=self.brand_4_pk)
        brand5: Brand = Brand.objects.get(pk=self.brand_5_pk)

        self.assertEqual(Brand.objects.count(), 5)

        self.assertIsNone(brand1.full_clean())
        self.assertIsNone(brand2.full_clean())
        self.assertIsNone(brand3.full_clean())
        self.assertIsNone(brand4.full_clean())
        self.assertIsNone(brand5.full_clean())

    def test_brand_update_validity(self) -> None:
        """Tests brand update integrity and validation"""

        Brand.objects.filter(pk=self.brand_4_pk).update(name='Brand 4 Updated')

        Brand.objects.filter(pk=self.brand_5_pk).update(name='Brand 5 Updated')

        for brand in Brand.objects.iterator():
            with self.subTest(brand=brand):
                self.assertIsNone(brand.full_clean())
