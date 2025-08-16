---
hide:
  - navigation
---

# To-Do Checklist

## To Be Evaluated

- [ ] Use of Rust for better processing
- [ ] Prefetch links for faster content load
- [ ] Implement `django.middleware.gzip.GZipMiddleware`
- [ ] User history of last actions, similar to Django's one
- [ ] Generate pseudo-random passwords as suggestion
- [ ] System migration to valid E2EE arch

## To Do

- [ ] Rewrite `save()` and `from_db` to base class with self logic
- [ ] Implement filter on listing page
- [ ] Export secrets with secure file
- [ ] Structure Timed Access for sharing
- [ ] Create Team Sharing
- [ ] Design locale and languages (pt-br, en)
- [ ] Apply chars count feedback in text inputs
- [ ] Redesign loadtests to a decent testing level
- [ ] Account recovery using 12-words recovery list

## Doing

- [ ] ...

## Done

- [x] Hide secret's data from staff and admin users
- [x] Implement `django-csp` for better security
- [x] Convert user's ID to UUIDv4
- [x] Create footer pages
- [x] Activate account checking both credentials and `account.models.ActivateAccountToken`
- [x] Redesign interfaces for a new era

<!--

### 🔐 Security by Design: Highlights

| Feature                     | Description                                                            |
| --------------------------- | ---------------------------------------------------------------------- |
| **Client-Side Encryption**  | AES-GCM with Argon2id-derived keys; zero plaintext sent to the server. |
| **Zero-Knowledge**          | sWarden cannot read or reset your secrets — not even if it wanted to.  |
| **End-to-End TLS**          | Enforced via `SECURE_SSL_REDIRECT` and `HSTS` headers.                 |
| **No Personal Data**        | You remain fully anonymous; no emails or identifiers collected.        |
| **No Third Parties**        | No analytics, ad networks, tracking libraries, or fingerprinting.      |
| **Open Source**             | Full source code available for community review and audit.             |
| **Regular Security Audits** | Black-box tested every quarter; published security reports.            |

---

### 🛑 Station 6: Failure Without Recovery

* If a user forgets their password or loses the `12-word recovery phrase`, **data is unrecoverable**.
* There are no support resets, recovery emails, or admin override keys.
* This is by design — **you control your encryption keys**.

---

## 📜 Final Note: Security Philosophy

sWarden’s architecture is guided by these principles:

* **Don’t collect what you can’t protect.**
* **Put the user in control of their data.**
* **Encrypt everything, always — at rest and in transit.**
* **Never trust the server with plaintext.**
* **Anonymity and privacy are not optional.**

---

## 🧩 View Source or Contribute

This system is open source under the [BSL License](https://github.com/swarden/core).

You can:

* View the code
* Report vulnerabilities
* Contribute to improvements

➡️ GitHub: [https://github.com/swarden/core](https://github.com/swarden/core)

---

Let me know if you'd like a matching **graphic** or **interactive SVG line** to represent this visually!
 -->
