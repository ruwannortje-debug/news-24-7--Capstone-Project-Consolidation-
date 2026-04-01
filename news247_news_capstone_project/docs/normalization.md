# Database normalization notes

## First normal form

Each table stores atomic values only. There are no repeating groups inside a single field.

## Second normal form

Non-key attributes depend on the whole key for each entity. For example, article content depends on the article identity, not on publisher membership or newsletter membership.

## Third normal form

Derived or unrelated data is separated into dedicated tables and relationships:

- `CustomUser` stores user identity and role information.
- `Publisher` stores publication metadata.
- `Article` stores article data and links to one author and optionally one publisher.
- `Newsletter` stores curated collections and uses a many-to-many link to articles.
- `ApprovedArticleLog` stores the approved-article event log.

This avoids duplication such as copying publisher details into every newsletter or subscriber details into every article.
