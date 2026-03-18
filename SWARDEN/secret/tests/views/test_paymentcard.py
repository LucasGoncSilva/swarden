from __future__ import annotations

from typing import TYPE_CHECKING

from account.models import User
from django.test import TestCase
from django.urls import reverse

from secret.models import (
    Bank,
    Brand,
    CardType,
    PaymentCard,
)
from secret.month.models import Month
from secret.views import (
    EMPTY_POST_MSG,
    MISSING_CRITICAL_INFO,
    SLUG_ALREADY_EXISTS_MSG,
)


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class BaseCardTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

        self.card_type_1: CardType = CardType.objects.create(name='Type 1')
        self.card_type_2: CardType = CardType.objects.create(name='Type 2')

        self.bank_1: Bank = Bank.objects.create(name='Bank 1')
        self.bank_2: Bank = Bank.objects.create(name='Bank 2')

        self.brand_1: Brand = Brand.objects.create(name='Brand 1')
        self.brand_2: Brand = Brand.objects.create(name='Brand 2')

        self.payment_card1: PaymentCard = PaymentCard.objects.create(
            owner=self.user,
            name='Personal Main Card',
            owners_name='TEST USER',
            card_type=self.card_type_1,
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank=self.bank_1,
            brand=self.brand_1,
            branch='123',
            account='123',
            password='123456',
            slug='bank-1-personal-main-card',
        )

        PaymentCard.objects.create(
            owner=self.user,
            name='Personal Second Card',
            owners_name='TEST USER',
            card_type=self.card_type_2,
            number='4002892240028922',
            expiration=Month(2028, 11),
            cvv='113',
            bank=self.bank_2,
            brand=self.brand_2,
            branch='123',
            account='123',
            password='123456',
            slug='bank-2-personal-second-card',
        )


class CardCreateViewsTestCase(BaseCardTestCase):
    def test_GET_create_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/new | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_create_view')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:card_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_create_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_create_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/new | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_create_view')
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Payment Card')

    def test_POST_anonymous_user_empty_form(self) -> None:
        """POST /secrets/payment-cards/new | anon user | empty form"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'), data={}
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:card_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'),
            data={},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_authenticated_user_empty_form(self) -> None:
        """POST /secrets/payment-cards/new | auth user | empty form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'),
            data={},
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, EMPTY_POST_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Payment Card')

    def test_POST_anonymous_user_empty_form_existing_secret(self) -> None:
        """GET /secrets/payment-cards/new | anon user | existent secret slug"""

        data: dict[str, str | User] = {
            'name': 'Personal Main Card',
            'owners_name': 'TEST USER',
            'card_type': self.card_type_1.pk,
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': self.bank_1.pk,
            'brand': self.brand_1.pk,
            'branch': '123',
            'account': '123',
            'password': '123456',
            'slug': 'bank-1-personal-main-card',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'), data=data
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login') + '?next=' + reverse('secret:card_create_view'),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_authenticated_user_empty_form_existing_secret(self) -> None:
        """POST /secrets/payment-cards/new | auth user | empty form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | User] = {
            'name': 'Personal Main Card',
            'owners_name': 'TEST USER',
            'card_type': self.card_type_1.pk,
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': self.bank_1.pk,
            'brand': self.brand_1.pk,
            'branch': '123',
            'account': '123',
            'password': '123456',
            'slug': 'bank-1-personal-main-card',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, SLUG_ALREADY_EXISTS_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Addition')
        self.assertEqual(res.context['model'], 'Payment Card')

    def test_POST_authenticated_user_valid_form(self) -> None:
        """POST /secrets/payment-cards/new | auth user | valid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | User] = {
            'name': 'Another Personal Main Card',
            'owners_name': 'TEST USER',
            'card_type': self.card_type_1.pk,
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': self.bank_1.pk,
            'brand': self.brand_1.pk,
            'branch': '123',
            'account': '123',
            'password': '123456',
            'slug': 'bank-1-another-personal-main-card',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('secret:card_create_view'),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Card/detail_view.html')


class CardListViewTestCase(BaseCardTestCase):
    def test_GET_list_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/ | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_list_view')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('account:login') + '?next=' + reverse('secret:card_list_view')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_list_view'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_list_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/ | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_list_view')
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/list_view.html')
        self.assertEqual(len(res.context['object_list']), 2)
        self.assertEqual(res.context['model_name'], 'Payment Cards')


class CardDetailViewTestCase(BaseCardTestCase):
    def test_GET_detail_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug> | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_detail_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:card_detail_view', kwargs={'slug': 'bank-1-personal-main-card'}
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_detail_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_detail_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug> | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_detail_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/Card/detail_view.html')
        self.assertEqual(
            res.context['object'],
            PaymentCard.objects.get(
                owner=User.objects.first(), slug='bank-1-personal-main-card'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_detail_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')


class CardUpdateViewTestCase(BaseCardTestCase):
    def test_GET_update_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/edit | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_update_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:card_update_view', kwargs={'slug': 'bank-1-personal-main-card'}
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_update_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_update_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/edit | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_update_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Payment Card')
        self.assertEqual(
            res.context['object'],
            PaymentCard.objects.get(
                owner=User.objects.first(), slug='bank-1-personal-main-card'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_update_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')

    def test_POST_authenticated_user_invalid_form(self) -> None:
        """POST /secrets/payment-cards/<slug:slug>/edit | auth user | invalid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | Month] = {
            'owner': self.user.pk,
            'name': 'Personal Main Card',
            'owners_name': 'TEST USER',
            'card_type': self.card_type_1.pk,
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': self.bank_1.pk,
            'brand': self.brand_1.pk,
            'branch': '123',
            'account': '123',
            'password': '123456',
            'slug': 'bank-1-personal-main-card',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:card_update_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, MISSING_CRITICAL_INFO, status_code=422)
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Payment Card')
        self.assertEqual(
            res.context['object'],
            PaymentCard.objects.get(
                owner=User.objects.first(), slug='bank-1-personal-main-card'
            ),
        )

    def test_POST_authenticated_user_existing_model(self) -> None:
        """POST /secrets/payment-cards/<slug:slug>/edit | auth user | model already exists"""  # noqa: E501

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | Month] = {
            'pk': self.payment_card1.pk,
            'owner': self.user.pk,
            'name': 'Personal Main Card',
            'owners_name': 'TEST USER',
            'card_type': self.card_type_2.pk,
            'number': '4002892240028922',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': self.bank_2.pk,
            'brand': self.brand_2.pk,
            'branch': '123',
            'account': '123',
            'password': '123456',
            'slug': 'bank-2-personal-second-card',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:card_update_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'secret/create_view.html')
        self.assertContains(res, SLUG_ALREADY_EXISTS_MSG, status_code=422)
        self.assertEqual(res.context['action'], 'Edition')
        self.assertEqual(res.context['model'], 'Payment Card')
        self.assertEqual(
            res.context['object'],
            PaymentCard.objects.get(
                owner=User.objects.first(), slug='bank-1-personal-main-card'
            ),
        )

    def test_POST_authenticated_user_success(self) -> None:
        """POST /secrets/payment-cards/<slug:slug>/edit | auth user | success"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        data: dict[str, str | bool | Month] = {
            'pk': self.payment_card1.pk,
            'owner': self.user.pk,
            'name': 'Personal Main Card',
            'owners_name': 'TEST USER',
            'card_type': self.card_type_1.pk,
            'number': '8922400289224002',
            'expiration_0': '11',
            'expiration_1': '2028',
            'cvv': '113',
            'bank': self.bank_1.pk,
            'brand': self.brand_1.pk,
            'branch': '123',
            'account': '123',
            'password': '123456',
            'slug': 'bank-1-personal-main-card',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse(
                'secret:card_update_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            ),
            data=data,
        )

        # Success response check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse('secret:card_detail_view', args=('bank-1-personal-main-card',))
        )


class CardDeleteViewTestCase(BaseCardTestCase):
    def test_GET_delete_anonymous_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/delete | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_delete_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            )
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res,
            reverse('account:login')
            + '?next='
            + reverse(
                'secret:card_delete_view', kwargs={'slug': 'bank-1-personal-main-card'}
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_delete_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            ),
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_delete_authenticated_user(self) -> None:
        """GET /secrets/payment-cards/<slug:slug>/delete | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse(
                'secret:card_delete_view',
                kwargs={'slug': 'bank-1-personal-main-card'},
            )
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'secret/delete_view.html')
        self.assertEqual(res.context['action'], 'Deletion')
        self.assertEqual(res.context['model'], 'Payment Card')
        self.assertEqual(
            res.context['object'],
            PaymentCard.objects.get(
                owner=User.objects.first(), slug='bank-1-personal-main-card'
            ),
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('secret:card_delete_view', kwargs={'slug': 'lasagna--double-pizza'})
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')
