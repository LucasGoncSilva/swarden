from uuid import UUID

from django.test import TestCase

from secret.models import NoteType


class NoteTypeTestCase(TestCase):
    def setUp(self) -> None:
        self.note_type_1_pk: UUID = NoteType.objects.create(name='NoteType 1').pk

        self.note_type_2_pk: UUID = NoteType.objects.create(name='NoteType 2').pk

        self.note_type_3_pk: UUID = NoteType.objects.create(name='NoteType 3').pk

        self.note_type_4_pk: UUID = NoteType.objects.create(name='NoteType 4').pk

        self.note_type_5_pk: UUID = NoteType.objects.create(name='NoteType 5').pk

    def test_note_type_instance_validity(self) -> None:
        """Tests note_type instance of correct class"""

        for note_type in NoteType.objects.iterator():
            with self.subTest(note_type=note_type):
                self.assertIsInstance(note_type, NoteType)

    def test_note_type_special_str_method_return(self) -> None:
        """Tests note_type return value of __str__ method"""

        note_type: NoteType = NoteType.objects.get(pk=self.note_type_1_pk)

        self.assertEqual(note_type.__str__(), 'NoteType 1')

    def test_note_type_key_value_assertion(self) -> None:
        """Tests note_type correct attribuition of value"""

        note_type1: NoteType = NoteType.objects.get(pk=self.note_type_1_pk)

        self.assertEqual(note_type1.name, 'NoteType 1')

    def test_note_type_create_validity(self) -> None:
        """Tests note_type creation integrity and validation"""

        note_type1: NoteType = NoteType.objects.get(pk=self.note_type_1_pk)
        note_type2: NoteType = NoteType.objects.get(pk=self.note_type_2_pk)
        note_type3: NoteType = NoteType.objects.get(pk=self.note_type_3_pk)
        note_type4: NoteType = NoteType.objects.get(pk=self.note_type_4_pk)
        note_type5: NoteType = NoteType.objects.get(pk=self.note_type_5_pk)

        self.assertEqual(NoteType.objects.count(), 5)

        self.assertIsNone(note_type1.full_clean())
        self.assertIsNone(note_type2.full_clean())
        self.assertIsNone(note_type3.full_clean())
        self.assertIsNone(note_type4.full_clean())
        self.assertIsNone(note_type5.full_clean())

    def test_note_type_update_validity(self) -> None:
        """Tests note_type update integrity and validation"""

        NoteType.objects.filter(pk=self.note_type_4_pk).update(
            name='NoteType 4 Updated'
        )

        NoteType.objects.filter(pk=self.note_type_5_pk).update(
            name='NoteType 5 Updated'
        )

        for note_type in NoteType.objects.iterator():
            with self.subTest(note_type=note_type):
                self.assertIsNone(note_type.full_clean())
