from uuid import UUID

from django.test import TestCase

from secret.models import Service


class ServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.service_1_pk: UUID = Service.objects.create(name='Service 1').pk

        self.service_2_pk: UUID = Service.objects.create(name='Service 2').pk

        self.service_3_pk: UUID = Service.objects.create(name='Service 3').pk

        self.service_4_pk: UUID = Service.objects.create(name='Service 4').pk

        self.service_5_pk: UUID = Service.objects.create(name='Service 5').pk

    def test_service_instance_validity(self) -> None:
        """Tests service instance of correct class"""

        for service in Service.objects.iterator():
            with self.subTest(service=service):
                self.assertIsInstance(service, Service)

    def test_service_special_str_method_return(self) -> None:
        """Tests service return value of __str__ method"""

        service: Service = Service.objects.get(pk=self.service_1_pk)

        self.assertEqual(service.__str__(), 'Service 1')

    def test_service_key_value_assertion(self) -> None:
        """Tests service correct attribuition of value"""

        service1: Service = Service.objects.get(pk=self.service_1_pk)

        self.assertEqual(service1.name, 'Service 1')

    def test_service_create_validity(self) -> None:
        """Tests service creation integrity and validation"""

        service1: Service = Service.objects.get(pk=self.service_1_pk)
        service2: Service = Service.objects.get(pk=self.service_2_pk)
        service3: Service = Service.objects.get(pk=self.service_3_pk)
        service4: Service = Service.objects.get(pk=self.service_4_pk)
        service5: Service = Service.objects.get(pk=self.service_5_pk)

        self.assertEqual(Service.objects.count(), 5)

        self.assertIsNone(service1.full_clean())
        self.assertIsNone(service2.full_clean())
        self.assertIsNone(service3.full_clean())
        self.assertIsNone(service4.full_clean())
        self.assertIsNone(service5.full_clean())

    def test_service_update_validity(self) -> None:
        """Tests service update integrity and validation"""

        Service.objects.filter(pk=self.service_4_pk).update(name='Service 4 Updated')

        Service.objects.filter(pk=self.service_5_pk).update(name='Service 5 Updated')

        for service in Service.objects.iterator():
            with self.subTest(service=service):
                self.assertIsNone(service.full_clean())
