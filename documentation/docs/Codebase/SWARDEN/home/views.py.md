# File: `views.py`

Role: :material-language-python: Python Source Code

Path: `SWARDEN.home`

No file docstring provided.

---

## Imports

### `#!py import HttpRequest`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpRequest
    ```

### `#!py import HttpResponse`

Path: `#!py django.http`

Category: trdparty

??? example "Snippet"

    ```py
    from django.http import HttpResponse
    ```

### `#!py import render`

Path: `#!py django.shortcuts`

Category: trdparty

??? example "Snippet"

    ```py
    from django.shortcuts import render
    ```

### `#!py import LoginCredential`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import LoginCredential
    ```

### `#!py import PaymentCard`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import PaymentCard
    ```

### `#!py import SecurityNote`

Path: `#!py secret.models`

Category: trdparty

??? example "Snippet"

    ```py
    from secret.models import SecurityNote
    ```



---

## Consts

### `#!py FAQ`

Type: `#!py dict[str, dict[str, str]]`

Value: `#!py {'General Questions': {'What types of information can I store in the system?': 'You can store three types of secrets: login credentials, payment cards, and free-form text notes. Each has predefined fields and categories for better organization.', 'Are my data encrypted?': 'Yes. All data is encrypted upon saving and only decrypted when you access them. Encryption combines the app’s private key with your password hash, making it readable only by you.', 'Can administrators see my secrets?': "No. The Django admin interface is disabled in production, and encryption keys differ by environment, so even database access doesn't expose decrypted data.", 'Does the system support two-factor authentication (2FA)?': 'Not at the moment. However, this may be considered for future development.', 'Is the codebase audited or externally reviewed for security?': 'Yes. Quarterly black-box security assessments simulate real-world attacks (Nmap, Hydra, Burp Suite, etc.). You can find the latest report via a link in the site footer.', 'How does the system handle identified vulnerabilities?': 'Vulnerabilities are triaged based on severity. The SECURITY.md file on GitHub provides guidance for reporting, and critical issues are addressed with immediate hotfixes.'}, 'Using the Application': {'Is the system available on mobile?': 'Yes. The system is fully responsive and works seamlessly on any modern browser, desktop or mobile.', 'Does it work offline?': 'No. An active internet connection is required to access your secrets.', 'Can I organize secrets using folders or tags?': 'Not currently. However, you can search secrets by the title you assign or the service name.', 'Does the app offer dark mode or accessibility options?': 'The UI uses a dark theme by default. Navigation is fully keyboard-accessible, though high-contrast themes are not yet available.', 'Does the system track me or sell my data?': 'Absolutely not. No personal information is used for tracking, marketing, or location purposes.', 'Are there search or filtering features?': 'Yes. You can quickly search secrets by name or associated service, making navigation simple even without folders.'}, 'Account and Subscription': {'Is the platform free to use?': 'Yes. The free plan allows up to 5 secrets per category. Paid users enjoy unlimited storage and full feature access.', 'Is there a password recovery system?': 'Yes. The system uses a 12-word recovery phrase, similar to crypto wallets. This is your only method for account recovery.', 'Can I change my recovery phrase?': 'No. The phrase is automatically and permanently generated when your account is created. It cannot be changed.', 'What happens if I lose both my password and recovery phrase?': 'Unfortunately, your account and data will be permanently lost. This is by design to ensure privacy and security.', 'How do I upgrade to a paid plan?': 'After creating a free account, select a monthly or discounted annual plan, and complete the payment via Mercado Pago (credit card, boleto, or Pix). Your access is upgraded automatically after payment.', 'Are subscriptions automatically renewed?': 'No. Subscriptions are not auto-renewed. Once a paid plan expires, access reverts to the free tier until manually renewed.', 'Can I delete my account and data?': 'Yes. You can permanently delete your account and all secrets from your user profile page. This also cancels your subscription.', 'Are there logs of login or access history?': 'Not yet. However, this feature is planned and will allow users to view activity history and access details.'}, 'Open Source': {'Is the source code available?': 'Yes. The entire codebase is open source and available on GitHub. A link to the repository is available in the site footer.', 'Can I contribute to the project?': 'Absolutely! Contributions are welcome. Just follow the guidelines in the README on GitHub.', 'Where can I report bugs or issues?': "Use GitHub Issues to report bugs, request features, or ask questions. It's the main support channel.", 'How can I suggest new features or ideas?': 'You can open an issue on GitHub to share ideas. All suggestions are reviewed and prioritized based on community needs.', 'Is there a public API available?': 'No. There is currently no API for third-party integrations, but this may be considered in the future.'}}`

??? example "Snippet"

    ```py
    FAQ: dict[str, dict[str, str]] = {'General Questions': {'What types of information can I store in the system?': 'You can store three types of secrets: login credentials, payment cards, and free-form text notes. Each has predefined fields and categories for better organization.', 'Are my data encrypted?': 'Yes. All data is encrypted upon saving and only decrypted when you access them. Encryption combines the app’s private key with your password hash, making it readable only by you.', 'Can administrators see my secrets?': "No. The Django admin interface is disabled in production, and encryption keys differ by environment, so even database access doesn't expose decrypted data.", 'Does the system support two-factor authentication (2FA)?': 'Not at the moment. However, this may be considered for future development.', 'Is the codebase audited or externally reviewed for security?': 'Yes. Quarterly black-box security assessments simulate real-world attacks (Nmap, Hydra, Burp Suite, etc.). You can find the latest report via a link in the site footer.', 'How does the system handle identified vulnerabilities?': 'Vulnerabilities are triaged based on severity. The SECURITY.md file on GitHub provides guidance for reporting, and critical issues are addressed with immediate hotfixes.'}, 'Using the Application': {'Is the system available on mobile?': 'Yes. The system is fully responsive and works seamlessly on any modern browser, desktop or mobile.', 'Does it work offline?': 'No. An active internet connection is required to access your secrets.', 'Can I organize secrets using folders or tags?': 'Not currently. However, you can search secrets by the title you assign or the service name.', 'Does the app offer dark mode or accessibility options?': 'The UI uses a dark theme by default. Navigation is fully keyboard-accessible, though high-contrast themes are not yet available.', 'Does the system track me or sell my data?': 'Absolutely not. No personal information is used for tracking, marketing, or location purposes.', 'Are there search or filtering features?': 'Yes. You can quickly search secrets by name or associated service, making navigation simple even without folders.'}, 'Account and Subscription': {'Is the platform free to use?': 'Yes. The free plan allows up to 5 secrets per category. Paid users enjoy unlimited storage and full feature access.', 'Is there a password recovery system?': 'Yes. The system uses a 12-word recovery phrase, similar to crypto wallets. This is your only method for account recovery.', 'Can I change my recovery phrase?': 'No. The phrase is automatically and permanently generated when your account is created. It cannot be changed.', 'What happens if I lose both my password and recovery phrase?': 'Unfortunately, your account and data will be permanently lost. This is by design to ensure privacy and security.', 'How do I upgrade to a paid plan?': 'After creating a free account, select a monthly or discounted annual plan, and complete the payment via Mercado Pago (credit card, boleto, or Pix). Your access is upgraded automatically after payment.', 'Are subscriptions automatically renewed?': 'No. Subscriptions are not auto-renewed. Once a paid plan expires, access reverts to the free tier until manually renewed.', 'Can I delete my account and data?': 'Yes. You can permanently delete your account and all secrets from your user profile page. This also cancels your subscription.', 'Are there logs of login or access history?': 'Not yet. However, this feature is planned and will allow users to view activity history and access details.'}, 'Open Source': {'Is the source code available?': 'Yes. The entire codebase is open source and available on GitHub. A link to the repository is available in the site footer.', 'Can I contribute to the project?': 'Absolutely! Contributions are welcome. Just follow the guidelines in the README on GitHub.', 'Where can I report bugs or issues?': "Use GitHub Issues to report bugs, request features, or ask questions. It's the main support channel.", 'How can I suggest new features or ideas?': 'You can open an issue on GitHub to share ideas. All suggestions are reviewed and prioritized based on community needs.', 'Is there a public API available?': 'No. There is currently no API for third-party integrations, but this may be considered in the future.'}}
    ```



---

## Classes

!!! info "NO CLASS DEFINED HERE"

---

## Functions

### `#!py def index`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def index(r: HttpRequest) -> HttpResponse:
        if r.user.is_authenticated:
            credentials: LoginCredential = r.user.credentials.all()
            cards: PaymentCard = r.user.cards.all()
            notes: SecurityNote = r.user.notes.all()
            return render(r, 'home/index.html', {'credentials': credentials[:3], 'cards': cards[:3], 'notes': notes[:3], 'credentials_counter': credentials.count(), 'cards_counter': cards.count(), 'notes_counter': notes.count()})
        return render(r, 'home/landing.html')
    ```

### `#!py def faq`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def faq(r: HttpRequest) -> HttpResponse:
        FAQ: dict[str, dict[str, str]] = {'General Questions': {'What types of information can I store in the system?': 'You can store three types of secrets: login credentials, payment cards, and free-form text notes. Each has predefined fields and categories for better organization.', 'Are my data encrypted?': 'Yes. All data is encrypted upon saving and only decrypted when you access them. Encryption combines the app’s private key with your password hash, making it readable only by you.', 'Can administrators see my secrets?': "No. The Django admin interface is disabled in production, and encryption keys differ by environment, so even database access doesn't expose decrypted data.", 'Does the system support two-factor authentication (2FA)?': 'Not at the moment. However, this may be considered for future development.', 'Is the codebase audited or externally reviewed for security?': 'Yes. Quarterly black-box security assessments simulate real-world attacks (Nmap, Hydra, Burp Suite, etc.). You can find the latest report via a link in the site footer.', 'How does the system handle identified vulnerabilities?': 'Vulnerabilities are triaged based on severity. The SECURITY.md file on GitHub provides guidance for reporting, and critical issues are addressed with immediate hotfixes.'}, 'Using the Application': {'Is the system available on mobile?': 'Yes. The system is fully responsive and works seamlessly on any modern browser, desktop or mobile.', 'Does it work offline?': 'No. An active internet connection is required to access your secrets.', 'Can I organize secrets using folders or tags?': 'Not currently. However, you can search secrets by the title you assign or the service name.', 'Does the app offer dark mode or accessibility options?': 'The UI uses a dark theme by default. Navigation is fully keyboard-accessible, though high-contrast themes are not yet available.', 'Does the system track me or sell my data?': 'Absolutely not. No personal information is used for tracking, marketing, or location purposes.', 'Are there search or filtering features?': 'Yes. You can quickly search secrets by name or associated service, making navigation simple even without folders.'}, 'Account and Subscription': {'Is the platform free to use?': 'Yes. The free plan allows up to 5 secrets per category. Paid users enjoy unlimited storage and full feature access.', 'Is there a password recovery system?': 'Yes. The system uses a 12-word recovery phrase, similar to crypto wallets. This is your only method for account recovery.', 'Can I change my recovery phrase?': 'No. The phrase is automatically and permanently generated when your account is created. It cannot be changed.', 'What happens if I lose both my password and recovery phrase?': 'Unfortunately, your account and data will be permanently lost. This is by design to ensure privacy and security.', 'How do I upgrade to a paid plan?': 'After creating a free account, select a monthly or discounted annual plan, and complete the payment via Mercado Pago (credit card, boleto, or Pix). Your access is upgraded automatically after payment.', 'Are subscriptions automatically renewed?': 'No. Subscriptions are not auto-renewed. Once a paid plan expires, access reverts to the free tier until manually renewed.', 'Can I delete my account and data?': 'Yes. You can permanently delete your account and all secrets from your user profile page. This also cancels your subscription.', 'Are there logs of login or access history?': 'Not yet. However, this feature is planned and will allow users to view activity history and access details.'}, 'Open Source': {'Is the source code available?': 'Yes. The entire codebase is open source and available on GitHub. A link to the repository is available in the site footer.', 'Can I contribute to the project?': 'Absolutely! Contributions are welcome. Just follow the guidelines in the README on GitHub.', 'Where can I report bugs or issues?': "Use GitHub Issues to report bugs, request features, or ask questions. It's the main support channel.", 'How can I suggest new features or ideas?': 'You can open an issue on GitHub to share ideas. All suggestions are reviewed and prioritized based on community needs.', 'Is there a public API available?': 'No. There is currently no API for third-party integrations, but this may be considered in the future.'}}
        return render(r, 'home/FAQ.html', {'FAQ': FAQ})
    ```

### `#!py def terms`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def terms(r: HttpRequest) -> HttpResponse:
        return render(r, 'home/terms.html')
    ```

### `#!py def privacy`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def privacy(r: HttpRequest) -> HttpResponse:
        return render(r, 'home/privacy.html')
    ```

### `#!py def cookies`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def cookies(r: HttpRequest) -> HttpResponse:
        return render(r, 'home/cookies.html')
    ```

### `#!py def security`

Type: `#!py function`

Decorators: `#!py None`

Args: `#!py r: HttpRequest`

Kwargs: `#!py None`

Return Type: `#!py HttpResponse`

??? quote "Docstring"

    No docstring provided.

??? example "Snippet"

    ```py
    def security(r: HttpRequest) -> HttpResponse:
        return render(r, 'home/security.html')
    ```



---

## Assertions

!!! info "NO ASSERT DEFINED HERE"
