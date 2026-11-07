# Security Policy

## Public profile repository

This repository is public because GitHub uses the username-matching repository to display the profile README. Treat every committed file, image, workflow, issue and log as public.

## Never commit

- API keys, access tokens, passwords, cookies or session data
- Private keys, certificates, recovery codes or credential exports
- Private user information, medical documents or confidential correspondence
- Local environment files or unredacted diagnostic logs

Use GitHub Actions secrets only for integrations that genuinely require credentials. The profile validation workflow uses the built-in GITHUB_TOKEN with contents: read. The optional RSS updater uses the built-in token for its README commit; no personal access token is required.

## Reporting a vulnerability

Do not publish credentials or sensitive exploit details in a public issue. Use GitHub's private vulnerability reporting feature if enabled, or contact the repository owner privately.

## Automated safeguards

The profile validation workflow:
- Checks tracked files for common high-confidence credential patterns and forbidden secret filenames.
- Runs unit tests for the optional RSS/Atom updater.
- Locks the approved Hero README block and Hero SVG blob.
- Validates local README image/link references, SVG XML, embedded active content, external SVG dependencies and asset budgets.

These checks reduce risk but cannot guarantee detection of every possible secret. Review every change before publishing.
