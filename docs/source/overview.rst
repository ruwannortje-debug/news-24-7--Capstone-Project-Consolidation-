Project Overview
================

News 24/7 is a Django-based news platform built for a role-based editorial
workflow. Readers can browse approved content and subscribe to publishers or
journalists, journalists can write articles and newsletters, and editors can
review and approve content before distribution.

Main features
-------------

- Custom user model with reader, editor, and journalist roles.
- Article drafting, editing, approval, and publication workflow.
- Newsletter creation with article selection.
- JWT-protected REST API for article and newsletter endpoints.
- Email notifications and approved-article logging via signal handlers.
- Sphinx documentation generated from project docstrings.
