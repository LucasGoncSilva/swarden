# ruff: noqa: E501

from pathlib import Path

from CORE.testcase import limit_memory
from django.conf import settings
from hypothesis import given
from hypothesis import settings as s
from hypothesis import strategies as st
from hypothesis.extra.django import SimpleTestCase

from crypt.algo import sWardenCryptography


class sWardenCryptographyTestCase(SimpleTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.key1: str = settings.CRYPTOGRAPHY_KEY
        cls.key2: str = settings.SYSTEM_PEPPER

        # Example Data:
        # 'v1$1$Qpk0DvuHsHrgpAZn$yHd96cTfgd9VWHAo8wC3qOn2gGfrkhiJts6JXJeEnRsOSpb6lA=='

    def _come_and_go(self, token: str) -> str:
        return sWardenCryptography.decrypt(
            sWardenCryptography.encrypt(token, self.key1, self.key2),
            self.key1,
            self.key2,
        )

    @limit_memory(KiB=4.6)  # Original: 295.78KiB
    def test_cryptography_simple_case(self) -> None:
        """Tests the simple process of encrypt and decrypt"""

        text: str = '1000 characters text' * 50

        processed: str = self._come_and_go(text)

        self.assertEqual(text, processed)

    @limit_memory(KiB=150.1)  # Original: 131215KiB
    def test_cryptography_mass_processing(self) -> None:
        """Tests the mass processing"""

        with open(Path(__file__).parent / 'sample.txt') as f:
            for i in f:
                decrypted: str = self._come_and_go(i)

                self.assertEqual(i, decrypted)

    def test_version_validation(self) -> None:
        """Tests invalid payload version"""

        with self.assertRaisesMessage(
            ValueError, 'Invalid payload of unmatched type/version'
        ):
            sWardenCryptography.decrypt('loremipsumdolorsitamet', self.key1, self.key2)

        with self.assertRaisesMessage(
            ValueError, 'Invalid payload of unmatched type/version'
        ):
            sWardenCryptography.decrypt('v0$0$random$stuff', self.key1, self.key2)

    def test_invalid_nonce(self) -> None:
        """Tests invalid payload's nonce"""

        with self.assertRaisesMessage(ValueError, 'Invalid Base64 in nonce'):
            data: str = (
                'v1$1$NONCE$yHd96cTfgd9VWHAo8wC3qOn2gGfrkhiJts6JXJeEnRsOSpb6lA=='
            )
            sWardenCryptography.decrypt(data, self.key1, self.key2)

        with self.assertRaisesMessage(ValueError, 'Invalid nonce length'):
            data: str = 'v1$1$Qpk0DvuHsHrgpAZnQpk0DvuHsHrgpAZn$yHd96cTfgd9VWHAo8wC3qOn2gGfrkhiJts6JXJeEnRsOSpb6lA=='
            sWardenCryptography.decrypt(data, self.key1, self.key2)

    def test_invalid_ciphertext(self) -> None:
        """Tests invalid payload's ciphertext"""

        with self.assertRaisesMessage(ValueError, 'Invalid Base64 in ciphertext'):
            data: str = 'v1$1$Qpk0DvuHsHrgpAZn$CIPHERTEXT'
            sWardenCryptography.decrypt(data, self.key1, self.key2)

        with self.assertRaisesMessage(
            ValueError, 'Decryption failed (wrong key or corrupted data)'
        ):
            data: str = 'v1$1$Qpk0DvuHsHrgpAZn$yHd96cTfgd9VWHAo8wC3qOn2gGfrkhiJts6JXJeEnRsOSpb6lA=='
            sWardenCryptography.decrypt(
                data, self.key1, 'just-a-banch-of-chars-mocking-a-key-and-the-dev'
            )

    @s(deadline=15000)
    @given(st.text(alphabet=st.characters(codec='utf-8'), min_size=1, max_size=256))
    def test_variable_inputs(self, token: str) -> None:
        """Tests variable possible inputs"""

        processed: str = self._come_and_go(token)

        self.assertEqual(token, processed)
