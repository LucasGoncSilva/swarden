import queue
import threading

from django.test import TestCase

from account.models import User
from utils import xor


class XORTestCase(TestCase):
    def setUp(self):
        self.password = User.objects.create_user(
            username='test_user',
            password='testing_password',
            email='test_user@example.com',
        ).password

        self.q = queue.Queue()
        self.num = 100_000
        # self.password = User.objects.get(pk=1).password

    def test_xor_null_value(self):
        """Tests if xor() retuns a NULL (\x00) value"""

        with open('secret/tests/sample.txt', 'r') as txt:
            lines = txt.readlines()

            for line in lines:
                data = line.strip()

                encrypted_data = xor(data, self.password[21:])

                decrypted_data = xor(encrypted_data, self.password[21:], encrypt=False)

                self.q.put(encrypted_data)
                self.q.put(decrypted_data)

        threading.Thread(target=self.assert_xor_null_value_in_data, daemon=True).start()
        self.q.join()

    def assert_xor_null_value_in_data(self):
        while True:
            data = self.q.get()

            self.assertNotIn('\x00', data)
            self.assertTrue(
                all(map(lambda x: x in range(0x110000), [ord(i) for i in data]))
            )

            self.q.task_done()
