from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.forms import LogInForm, RecoveryTestForm, RecoveryWordlistForm
from account.models import ActivationAccountToken, RecoveryPhrase, User


if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class BaseAccountTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            username='username',
            password='longpassphrase',
            is_active=True,
        )

        self.REGISTER_URL: str = reverse('account:register')
        self.WORDLIST: str = reverse('account:wordlist')
        self.LOGIN_URL: str = reverse('account:login')
        self.LOGOUT_URL: str = reverse('account:logout')
        self.RECOVERY_URL: str = reverse('account:recovery')


class RegisterViewTestCase(BaseAccountTestCase):
    def test_GET_authenticated_user(self) -> None:
        """GET /account/register | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.REGISTER_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            self.REGISTER_URL, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_GET_anonymous_user(self) -> None:
        """GET /account/register | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.REGISTER_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/register.html')

    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /account/register | anon user | invalid form"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.REGISTER_URL,
            data={'captcha_0': 'dummy-value', 'captcha_1': 'PASSED'},
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertContains(res, 'Please fill the form correctly.', status_code=422)

    def test_POST_anonymous_user_different_passphrases(self) -> None:
        """POST /account/register | anon user | different passphrases"""

        data: dict[str, str] = {
            'username': 'username',
            'passphrase': '1234123412341234',
            'passphrase2': '1234567812345678',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.REGISTER_URL, data=data)

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertContains(res, 'Passphrases does not match.', status_code=422)

    def test_POST_anonymous_user_existing_username(self) -> None:
        """POST /account/register | anon user | username already exists"""

        data: dict[str, str] = {
            'username': 'username',
            'passphrase': 'longpassphrase',
            'passphrase2': 'longpassphrase',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.REGISTER_URL, data=data)

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/register.html')
        self.assertContains(res, 'Invalid or unavailable username.', status_code=422)

    def test_POST_anonymous_user_valid_form(self) -> None:
        """POST /account/register | anon user | valid form"""

        data: dict[str, str] = {
            'username': 'newusername',
            'passphrase': 'longpassphrase',
            'passphrase2': 'longpassphrase',
            'captcha_0': 'dummy-value',
            'captcha_1': 'PASSED',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.REGISTER_URL, data=data, follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/activate_account.html')
        self.assertContains(
            res,
            'Account created. Activate it below.',
        )


class ActivateAccountViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user_no_parameter(self) -> None:
        """GET /account/activate/ | anon user | no parameters"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate_no_parameter')
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate_no_parameter'), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

    def test_GET_anonymous_user_missing_token(self) -> None:
        """GET /account/activate/<Any> | anon user | missing token"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate_no_token', args=('404',))
        )

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate_no_token', args=('404',)), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/landing.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /account/activate/<uidb64>/<token> | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        user: User = cast(User, User.objects.first())

        uidb64_pk: str = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value])
        )

        # Success response check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value]), follow=True
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_GET_anonymous_user(self) -> None:
        """GET /account/activate/<uidb64>/<token> | anonymous user"""

        user: User = cast(User, User.objects.first())

        uidb64_pk: str = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            reverse('account:activate', args=[uidb64_pk, token.value])
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/activate_account.html')
        self.assertIsInstance(res.context['form'], LogInForm)

    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /account/activate/<uidb64>/<token> | anon user | invalid form"""

        User.objects.filter(pk=self.user.pk).update(is_active=False)

        user: User = cast(User, User.objects.first())

        uidb64_pk: str = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        data: dict[str, str] = {
            'username': 'username',
            'passphrase': '1234',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('account:activate', args=[uidb64_pk, token.value]),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/activate_account.html')
        self.assertContains(res, 'Please fill the form correctly.', status_code=422)

    def test_POST_anonymous_user_invalid_uidb64(self) -> None:
        """POST /account/activate/<uidb64>/<token> | anon user | invalid uidb64"""

        User.objects.filter(pk=self.user.pk).update(is_active=False)

        user: User = cast(User, User.objects.first())

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        data: dict[str, str] = {
            'username': 'username',
            'passphrase': 'longpassphrase',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('account:activate', args=('uidb64_pk', token.value)),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')

    def test_POST_anonymous_user_invalid_activating_token(self) -> None:
        """POST /account/activate/<uidb64>/<token> | anon user | invalid token"""

        User.objects.filter(pk=self.user.pk).update(is_active=False)

        user: User = cast(User, User.objects.first())

        uidb64_pk: str = urlsafe_base64_encode(force_bytes(user.pk))

        data: dict[str, str] = {
            'username': 'username',
            'passphrase': 'longpassphrase',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('account:activate', args=[uidb64_pk, 'token.value']),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 404)
        self.assertTemplateUsed(res, 'err/error_template.html')

    def test_POST_anonymous_user_not_found_username(self) -> None:
        """POST /account/activate/<uidb64>/<token> | anon user | username not found"""

        User.objects.filter(pk=self.user.pk).update(is_active=False)

        user: User = cast(User, User.objects.first())

        uidb64_pk: str = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        data: dict[str, str] = {
            'username': 'useruser',
            'passphrase': 'longpassphrase',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('account:activate', args=[uidb64_pk, token.value]),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/activate_account.html')
        self.assertContains(res, 'Invalid username and/or passphrase', status_code=422)

    def test_POST_anonymous_user_success(self) -> None:
        """POST /account/activate/<uidb64>/<token> | anon user | success"""

        User.objects.filter(pk=self.user.pk).update(is_active=False)

        user: User = cast(User, User.objects.first())

        uidb64_pk: str = urlsafe_base64_encode(force_bytes(user.pk))

        token: ActivationAccountToken = ActivationAccountToken.objects.create(
            value='x' * 64,
            user=user,
            used=False,
        )

        data: dict[str, str] = {
            'username': 'username',
            'passphrase': 'longpassphrase',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            reverse('account:activate', args=[uidb64_pk, token.value]),
            data=data,
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/wordlist.html')
        self.assertContains(
            res,
            'Account activated successfully!',
        )


class WordlistViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /account/wordlist | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:login') + '?next=' + self.WORDLIST)

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST, follow=True)

        # Success redirect check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user_existing_recovery(self) -> None:
        """GET /account/wordlist | auth user | recovery phrase exists"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        words: str = settings.MNEMONIC.generate(strength=128)

        RecoveryPhrase.objects.create(
            user=self.user,
            phrase_hash=make_password(words),
            fingerprint=RecoveryPhrase.generate_fingerprint(words),
            is_active=True,
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST, follow=True)

        # Success redirect check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_GET_authenticated_user_success(self) -> None:
        """GET /account/wordlist | auth user | success"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST)

        # Success redirect check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/wordlist.html')
        self.assertIsInstance(res.context['form'], RecoveryTestForm)
        self.assertIsInstance(res.context['wordlist'], dict)
        self.assertListEqual(list(res.context['wordlist'].keys()), list(range(1, 13)))
        self.assertIsInstance(res.context['test_order'], dict)

        for k, v in res.context['test_order'].items():
            with self.subTest(word=v):
                self.assertEqual(res.context['wordlist'][k], v)

    def test_POST_authenticated_user_invalid_form(self) -> None:
        """POST /account/wordlist | auth user | invalid form"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST)

        data: dict[str, str] = {
            'not_word1': 'lorem',
            'not_word2': 'lorem',
            'not_word3': 'lorem',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.WORDLIST, data=data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:wordlist'))

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.WORDLIST, data=data, follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/wordlist.html')
        self.assertContains(
            res,
            'Please fill the form correctly.',
        )

    def test_POST_authenticated_user_wrong_form_words(self) -> None:
        """POST /account/wordlist | auth user | wrong test words"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST)

        data: dict[str, str] = {
            'word1': 'lorem',
            'word2': 'lorem',
            'word3': 'lorem',
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.WORDLIST, data=data)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('account:wordlist'))

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.WORDLIST, data=data, follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/wordlist.html')
        self.assertContains(
            res,
            'You missed. Pay attention now.',
        )

    def test_POST_authenticated_user_success(self) -> None:
        """POST /account/wordlist | auth user | success"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.WORDLIST)

        test_words: tuple[str, str, str] = tuple(res.context['test_order'].values())
        word1, word2, word3 = test_words

        data: dict[str, str] = {
            'word1': word1,
            'word2': word2,
            'word3': word3,
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.WORDLIST, data=data, follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertContains(
            res,
            '12-words recovery list completed successfully. Do not lose it.',
        )


class LoginViewTestCase(BaseAccountTestCase):
    def test_GET_authenticated_user(self) -> None:
        """GET /account/login | authenticated user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.LOGIN_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.LOGIN_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_GET_anonymous_user(self) -> None:
        """GET /account/login | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.LOGIN_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /account/login | anon user | invalid form"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.LOGIN_URL,
            {'username': 'username', 'passphrase': 'short'},
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/login.html')
        self.assertContains(res, 'Please fill the form correctly.', status_code=422)

    def test_GET_anonymous_user_user_is_None(self) -> None:
        """GET /account/login | anon user | user is None"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.LOGIN_URL,
            {
                'username': 'fake_user',
                'passphrase': 'longpassphrase',
            },
        )

        # Success response check
        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_anonymous_user_success(self) -> None:
        """GET /account/login | anon user | success"""

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.LOGIN_URL,
            {
                'username': 'username',
                'passphrase': 'longpassphrase',
            },
            follow=True,
        )

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')


class RecoveryViewTestCase(BaseAccountTestCase):
    def test_GET_authenticated_user(self) -> None:
        """GET /account/recovery | auth user | redirects"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.RECOVERY_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('home:index'))

        res: _MonkeyPatchedWSGIResponse = self.client.get(
            self.RECOVERY_URL, follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')

    def test_GET_anonymous_user(self) -> None:
        """GET /account/recovery | anonymous user"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.RECOVERY_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/recovery.html')
        self.assertIsInstance(res.context['form'], RecoveryWordlistForm)

    def test_POST_anonymous_user_invalid_form(self) -> None:
        """POST /account/recovery | anon user | invalid form"""

        words: str = settings.MNEMONIC.generate(strength=128)

        RecoveryPhrase.objects.create(
            user=self.user,
            phrase_hash=make_password(words),
            fingerprint=RecoveryPhrase.generate_fingerprint(words),
            is_active=True,
        )

        data: dict[str, str] = {
            f'word{i - 1}': word for i, word in enumerate(words.split(), start=1)
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.RECOVERY_URL, data=data)

        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/recovery.html')
        self.assertIsInstance(res.context['form'], RecoveryWordlistForm)
        self.assertContains(res, 'Please fill the form correctly.', status_code=422)

    def test_POST_anonymous_user_inexisting_recovery_words(self) -> None:
        """POST /account/recovery | anon user | falsy words"""

        words: str = settings.MNEMONIC.generate(strength=128)

        RecoveryPhrase.objects.create(
            user=self.user,
            phrase_hash=make_password(words),
            fingerprint=RecoveryPhrase.generate_fingerprint(words),
            is_active=True,
        )

        data: dict[str, str] = {
            f'word{i}': f'{word.replace("e", "a")}'
            for i, word in enumerate(words.split(), start=1)
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.RECOVERY_URL, data=data)

        self.assertEqual(res.status_code, 422)
        self.assertTemplateUsed(res, 'account/recovery.html')
        self.assertIsInstance(res.context['form'], RecoveryWordlistForm)
        self.assertContains(
            res,
            'Something went wrong with provided words. Please review them.',
            status_code=422,
        )

    def test_POST_anonymous_user_success(self) -> None:
        """POST /account/recovery | anon user | success"""

        words: str = settings.MNEMONIC.generate(strength=128)

        RecoveryPhrase.objects.create(
            user=self.user,
            phrase_hash=make_password(words),
            fingerprint=RecoveryPhrase.generate_fingerprint(words),
            is_active=True,
        )

        data: dict[str, str] = {
            f'word{i}': f'{word}' for i, word in enumerate(words.split(), start=1)
        }

        res: _MonkeyPatchedWSGIResponse = self.client.post(
            self.RECOVERY_URL, data=data, follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'home/index.html')
        self.assertContains(
            res,
            'Success on recovery list login!',
        )


class LogoutViewTestCase(BaseAccountTestCase):
    def test_GET_anonymous_user(self) -> None:
        """GET /account/logout | anon user | redirects to login"""

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.LOGOUT_URL)

        # Success redirect check
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.LOGIN_URL + '?next=' + self.LOGOUT_URL)

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.LOGOUT_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')

    def test_GET_authenticated_user(self) -> None:
        """GET /account/logout | anonymous user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.get(self.LOGOUT_URL)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/logout.html')

    def test_POST_authenticated_user(self) -> None:
        """POST /account/logout | anonymous user"""

        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.LOGOUT_URL)

        self.assertEqual(res.status_code, 302)
        # Confirm user login
        self.assertTrue(
            self.client.login(username='username', password='longpassphrase')
        )

        res: _MonkeyPatchedWSGIResponse = self.client.post(self.LOGOUT_URL, follow=True)

        # Success response check
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'account/login.html')
