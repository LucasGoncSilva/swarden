from __future__ import annotations

from typing import TYPE_CHECKING

from account.models import User
from django.test import TestCase
from django.urls import reverse
from secret.models import (
    Bank,
    Brand,
    CardType,
    LoginCredential,
    NoteType,
    PaymentCard,
    SecurityNote,
    Service,
)
from secret.month.models import Month


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class HomeViewsTestCase(TestCase):
    def setUp(self) -> None:
        user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

        self.card_type: CardType = CardType.objects.create(name='Type')

        self.bank: Bank = Bank.objects.create(name='Bank')

        self.brand: Brand = Brand.objects.create(name='Brand')

        self.service: Service = Service.objects.create(name='Service')

        self.note_type: NoteType = NoteType.objects.create(name='Type')

        PaymentCard.objects.create(
            owner=user,
            name='Personal Main Card',
            owners_name='TEST USER',
            card_type=self.card_type,
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank=self.bank,
            brand=self.brand,
            branch='123',
            account='123',
            password='123456',
            slug='bank-personal-main-card',
        )

        LoginCredential.objects.create(
            owner=user,
            service=self.service,
            name='Personal Main Account',
            slug='service-personal-main-account',
            third_party_login=False,
            third_party_login_name='-----',
            login='night_monkey123@gmail.com',
            password='ilovemenotyou',
        )

        LoginCredential.objects.create(
            owner=user,
            service=self.service,
            name='Little Fries',
            slug='service-little-fries',
            third_party_login=True,
            third_party_login_name='Personal Main Account',
            login='-----',
            password='-----',
        )

        SecurityNote.objects.create(
            owner=user,
            title='How to draw an apple',
            slug='how-to-draw-an-apple',
            note_type=self.note_type,
            content='Just draw an apple tree and erase the tree.',
        )

    def test_GET_anonymous_user(self) -> None:
        """GET / | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

    def test_GET_authenticated_user(self) -> None:
        """GET / | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:index'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertIn('cards', res.context)
        self.assertIn('credentials', res.context)
        self.assertIn('notes', res.context)
        self.assertEqual(len(res.context['cards']), 1)
        self.assertEqual(len(res.context['credentials']), 2)
        self.assertEqual(len(res.context['notes']), 1)


class FAQViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /FAQ | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:faq'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/FAQ.html')
        self.assertEqual(len(res.context['FAQ']['General Questions']), 6)
        self.assertEqual(len(res.context['FAQ']['Using the Application']), 6)
        self.assertEqual(len(res.context['FAQ']['Account and Subscription']), 8)
        self.assertEqual(len(res.context['FAQ']['Open Source']), 5)

    def test_GET_authenticated_user(self) -> None:
        """GET /FAQ | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:faq'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/FAQ.html')
        self.assertEqual(len(res.context['FAQ']['General Questions']), 6)
        self.assertEqual(len(res.context['FAQ']['Using the Application']), 6)
        self.assertEqual(len(res.context['FAQ']['Account and Subscription']), 8)
        self.assertEqual(len(res.context['FAQ']['Open Source']), 5)


class TermsViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /terms | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:terms'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/terms.html')
        self.assertContains(res, '1. Introduction')
        self.assertContains(res, '2. Eligibility')
        self.assertContains(res, '3. Account and Access')
        self.assertContains(res, '4. Service Description')
        self.assertContains(res, '5. Data and Privacy')
        self.assertContains(res, '6. User Responsibilities')
        self.assertContains(res, '7. Security Practices')
        self.assertContains(res, '8. Limitations of Liability')
        self.assertContains(res, '9. Modifications to the Service')
        self.assertContains(res, '10. Subscription and Billing')
        self.assertContains(res, '11. Termination')
        self.assertContains(res, '12. Governing Law')
        self.assertContains(res, '13. Open Source Notice')
        self.assertContains(res, '14. Contact')

    def test_GET_authenticated_user(self) -> None:
        """GET /terms | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:terms'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/terms.html')
        self.assertContains(res, '1. Introduction')
        self.assertContains(res, '2. Eligibility')
        self.assertContains(res, '3. Account and Access')
        self.assertContains(res, '4. Service Description')
        self.assertContains(res, '5. Data and Privacy')
        self.assertContains(res, '6. User Responsibilities')
        self.assertContains(res, '7. Security Practices')
        self.assertContains(res, '8. Limitations of Liability')
        self.assertContains(res, '9. Modifications to the Service')
        self.assertContains(res, '10. Subscription and Billing')
        self.assertContains(res, '11. Termination')
        self.assertContains(res, '12. Governing Law')
        self.assertContains(res, '13. Open Source Notice')
        self.assertContains(res, '14. Contact')


class PrivacyViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /privacy | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:privacy'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/privacy.html')
        self.assertContains(res, '1. Introduction')
        self.assertContains(res, '2. Information We Do Not Collect')
        self.assertContains(res, '3. Information We Collect')
        self.assertContains(res, '4. Use of Information')
        self.assertContains(res, '5. Cookies and Tracking')
        self.assertContains(res, '6. Data Security')
        self.assertContains(res, '7. User Control and Access')
        self.assertContains(res, '8. Data Sharing and Disclosure')
        self.assertContains(res, '9. Children’s Privacy')
        self.assertContains(res, '10. International Data Transfers')
        self.assertContains(res, '11. Legal Basis for Data Processing')
        self.assertContains(res, '12. Changes to This Policy')
        self.assertContains(res, '13. Contact')

    def test_GET_authenticated_user(self) -> None:
        """GET /privacy | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:privacy'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/privacy.html')
        self.assertContains(res, '1. Introduction')
        self.assertContains(res, '2. Information We Do Not Collect')
        self.assertContains(res, '3. Information We Collect')
        self.assertContains(res, '4. Use of Information')
        self.assertContains(res, '5. Cookies and Tracking')
        self.assertContains(res, '6. Data Security')
        self.assertContains(res, '7. User Control and Access')
        self.assertContains(res, '8. Data Sharing and Disclosure')
        self.assertContains(res, '9. Children’s Privacy')
        self.assertContains(res, '10. International Data Transfers')
        self.assertContains(res, '11. Legal Basis for Data Processing')
        self.assertContains(res, '12. Changes to This Policy')
        self.assertContains(res, '13. Contact')


class CookiesViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /cookies | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:cookies'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/cookies.html')
        self.assertContains(res, '1. Introduction')
        self.assertContains(res, '2. Our Use of Cookies')
        self.assertContains(res, '3. Cookie Table')
        self.assertContains(res, '4. No Third-Party Cookies')
        self.assertContains(res, '5. Your Cookie Controls')
        self.assertContains(res, '6. Legal Compliance')
        self.assertContains(res, '7. Contact')

    def test_GET_authenticated_user(self) -> None:
        """GET /cookies | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:cookies'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/cookies.html')
        self.assertContains(res, '1. Introduction')
        self.assertContains(res, '2. Our Use of Cookies')
        self.assertContains(res, '3. Cookie Table')
        self.assertContains(res, '4. No Third-Party Cookies')
        self.assertContains(res, '5. Your Cookie Controls')
        self.assertContains(res, '6. Legal Compliance')
        self.assertContains(res, '7. Contact')


class SecurityViewsTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

    def test_GET_anonymous_user(self) -> None:
        """GET /security | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:security'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/security.html')
        self.assertContains(res, 'Browser')
        self.assertContains(res, 'Local Cryptography')
        self.assertContains(res, 'HTTPS Transmission')
        self.assertContains(res, 'Middlewares')
        self.assertContains(res, 'Backend Logic')
        self.assertContains(res, 'Database (Encrypted at Rest)')
        self.assertContains(res, 'Response to Client')

    def test_GET_authenticated_user(self) -> None:
        """GET /security | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(reverse('home:security'))

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/security.html')
        self.assertContains(res, 'Browser')
        self.assertContains(res, 'Local Cryptography')
        self.assertContains(res, 'HTTPS Transmission')
        self.assertContains(res, 'Middlewares')
        self.assertContains(res, 'Backend Logic')
        self.assertContains(res, 'Database (Encrypted at Rest)')
        self.assertContains(res, 'Response to Client')
