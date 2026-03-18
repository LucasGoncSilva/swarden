from uuid import UUID

from account.models import User
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.test import TestCase
from django.urls import reverse

from secret.models import (
    NoteType,
    SecurityNote,
)


class SecurityNoteTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='user',
            password='longpassphrase',
        )

        self.note_type_1: NoteType = NoteType.objects.create(name='Type 1')
        self.note_type_2: NoteType = NoteType.objects.create(name='Type 2')

        # Object 1
        self.security_note_1_pk: UUID = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            note_type=self.note_type_1,
            content='Just draw an apple tree and erase the tree.',
        ).pk  # Correct object

        # Object 2
        self.security_note_2_pk: UUID = SecurityNote.objects.create(
            owner=self.user,
            title='How not to draw a tree',
            slug='how-not-to-draw-a-tree',
            note_type=self.note_type_2,
            content='Just not draw an apple tree and not erase the apples.',
        ).pk  # Correct object

        # Object 3
        self.security_note_3_pk: UUID = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw a tree',
            slug='howtodrawatree',  # 'how-to-draw-a-tree'
            note_type=self.note_type_1,
            content='Just draw an apple tree and erase the apples.',
        ).pk

        # Object 4
        self.security_note_4_pk: UUID = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple tree',
            slug='how-to-draw-an-apple-tree',
            note_type=self.note_type_1,
            content='x' * 1001,  # Length out of range
        ).pk

        # Object 5
        self.security_note_5_pk: UUID = SecurityNote.objects.create(
            owner=self.user,
            title='How to draw an apple tree leaf',
            slug='how-to-draw-an-apple-tree-leaf',
            note_type=self.note_type_1,
        ).pk  # Missing/empty content field

    def test_note_instance_validity(self) -> None:
        """Tests note instance of correct class"""

        for note in SecurityNote.objects.iterator():
            with self.subTest(note=note):
                self.assertIsInstance(note, SecurityNote)

    def test_note_special_str_method_return(self) -> None:
        """Tests note return value of __str__ method"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1_pk)

        self.assertEqual(note1.__str__(), f'{note1.owner.username} | {note1.title}')

    def test_note_absolute_url_method_return(self) -> None:
        """Tests note return value of get_absolute_url method"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1_pk)

        self.assertEqual(
            note1.get_absolute_url(),
            reverse('secret:note_detail_view', args=(note1.slug,)),
        )

    def test_note_key_value_assertion(self) -> None:
        """Tests note correct attribuition of value"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1_pk)

        self.assertEqual(note1.title, 'How to draw an apple')
        self.assertEqual(note1.slug, 'how-to-draw-an-apple')
        self.assertEqual(note1.note_type, self.note_type_1)
        self.assertEqual(note1.content, 'Just draw an apple tree and erase the tree.')

    def test_note_user_foreign_key_validity(self) -> None:
        """Tests note user foreign key validation"""

        note1_owner: User = SecurityNote.objects.get(pk=self.security_note_1_pk).owner

        self.assertEqual(note1_owner, self.user)

    def test_note_create_validity(self) -> None:
        """Tests note creation integrity and validation"""

        note1: SecurityNote = SecurityNote.objects.get(pk=self.security_note_1_pk)
        note2: SecurityNote = SecurityNote.objects.get(pk=self.security_note_2_pk)
        note3: SecurityNote = SecurityNote.objects.get(pk=self.security_note_3_pk)
        note4: SecurityNote = SecurityNote.objects.get(pk=self.security_note_4_pk)
        note5: SecurityNote = SecurityNote.objects.get(pk=self.security_note_5_pk)

        self.assertEqual(SecurityNote.objects.count(), 5)

        note1.full_clean()
        note2.full_clean()

        with self.assertRaises(ValidationError):
            note3.full_clean()

        with self.assertRaises(ValidationError):
            note4.full_clean()

        with self.assertRaises(ValidationError):
            note5.full_clean()

    def test_note_update_validity(self) -> None:
        """Tests note update integrity and validation"""

        SecurityNote.objects.filter(pk=self.security_note_3_pk).update(
            slug='how-to-draw-a-tree'
        )
        SecurityNote.objects.filter(pk=self.security_note_4_pk).update(
            content='Draw a tree and then the apples.'
        )
        SecurityNote.objects.filter(pk=self.security_note_5_pk).update(
            content='Draw an apple tree and then erase the apples and the tree.'
        )

        for note in SecurityNote.objects.iterator():
            with self.subTest(note=note):
                self.assertIsNone(note.full_clean())

    def test_note_delete_validity(self) -> None:
        """Tests note correct deletion"""

        for note in SecurityNote.objects.iterator():
            with self.subTest(note=note):
                try:
                    note.full_clean()
                except ValidationError:
                    note.delete()

        self.assertEqual(SecurityNote.objects.count(), 2)

    def test_note_db_exception_raises(self) -> None:
        """Tests note correct integrity and validation with raised exceptions"""

        # Expecting raises
        raise_kwargs: dict[str, dict[str, User | NoteType | str]] = {
            'note1': {'owner': self.user},
            'note2': {'title': 'A Title'},
            'note3': {'slug': 'a-title'},
            'note4': {'note_type': self.note_type_1},
            'note5': {'content': 'A regular content'},
            'note6': {'owner': self.user, 'title': 'A Title'},
            'note7': {'owner': self.user, 'slug': 'a-title'},
            'note8': {'owner': self.user, 'content': 'A regular content'},
            'note9': {'owner': self.user, 'note_type': self.note_type_1},
            'note10': {'owner': self.user, 'title': 'A Title', 'slug': 'a-title'},
            'note11': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
            },
            'note12': {
                'owner': self.user,
                'title': 'A Title',
                'note_type': self.note_type_1,
            },
            'note13': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'slug': 'a-title',
            },
            'note14': {
                'owner': self.user,
                'title': 'x' * 41,
                'content': 'A regular content',
                'slug': 'a-title',
                'note_type': self.note_type_1,
            },
            'note15': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'x' * 1001,
                'slug': 'a-title',
                'note_type': self.note_type_1,
            },
            'note16': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'slug': 'x' * 51,
                'note_type': self.note_type_1,
            },
        }

        for scenario in raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                with self.assertRaises(ValidationError):
                    with atomic():
                        instance: SecurityNote = SecurityNote(**raise_kwargs[scenario])
                        instance.full_clean()

        # Not expecting raises
        no_raise_kwargs: dict[str, dict[str, str | User | NoteType]] = {
            'note1': {
                'owner': self.user,
                'title': 'A Title',
                'content': 'A regular content',
                'note_type': self.note_type_1,
                'slug': 'a-title',
            },
            'note2': {
                'owner': self.user,
                'title': 'x ' * 20,
                'content': 'x' * 300,
                'note_type': self.note_type_1,
                'slug': 'x-' * 19 + 'x',
            },
        }

        for scenario in no_raise_kwargs.keys():
            with self.subTest(scenario=scenario):
                instance: SecurityNote = SecurityNote(**no_raise_kwargs[scenario])
                instance.full_clean()
