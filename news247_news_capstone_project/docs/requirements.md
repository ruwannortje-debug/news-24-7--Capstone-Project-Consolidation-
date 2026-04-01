# Functional and non-functional requirements

## Functional requirements

- Readers can register, log in, browse approved articles, and read newsletters.
- Readers can subscribe to publishers and individual journalists.
- Journalists can create, update, and delete their own articles.
- Journalists can create newsletters and curate articles inside newsletters.
- Editors can review pending articles and approve them.
- Approved articles trigger email delivery to subscribers.
- Approved articles are logged through the internal `/api/approved/` endpoint.
- API clients can authenticate with JWT and retrieve approved or subscribed articles.

## Non-functional requirements

- Clean, readable, modular Django code.
- PEP 8 formatting and docstrings on key components.
- Defensive access control and validation.
- Responsive UI that works on desktop and mobile.
- Automated tests for both successful and failed API requests.
- Database design normalized to avoid duplication.
- MariaDB-ready configuration for final submission.
