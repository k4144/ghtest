## Cassette Sanitization

Recorded VCR cassettes often contain user identifiers and API tokens. After
generating tests, scrub the cassette directory before committing:

```bash
python -m ghtest.cassette_sanitizer tests/cassettes
```

or specify any directory/file paths to sanitize. The sanitizer:

- removes URL-heavy metadata and IDs,
- masks user/repo names, emails, etc.,
- rewrites auth headers so prefixes (e.g. `Bearer `) remain while the token body
  is replaced with placeholder characters,
- parses JSON bodies inside the cassette and scrubs nested fields as well.

Workflow tip:

1. Generate tests/cassettes with `ghtest`.
2. Run the sanitizer across the cassette directory.
3. Re-run the generated tests (using the sanitized cassettes) to refresh the
   captured expectations without hitting the network again.
