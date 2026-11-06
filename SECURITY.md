# Security Policy

## Public profile repository

This repository is intentionally public because GitHub requires a public username-matching repository to display a public profile README. Treat every committed file, image, workflow, issue and log as public.

## Never commit

- API keys, access tokens, passwords, cookies or session data
- Private keys, certificates, recovery codes or credential exports
- Private user information, medical documents or confidential correspondence
- Local environment files or unredacted diagnostic logs

Use GitHub Actions secrets for credentials required by automation. The profile workflows use only the repository-scoped built-in `GITHUB_TOKEN`; no personal access token is required.

## Reporting a vulnerability

Do not publish credentials or sensitive exploit details in a public issue. Use GitHub's private vulnerability reporting feature if it is enabled for this repository, or contact the repository owner privately.

## Automated safeguards

The profile validation workflow checks repository-tracked text files for common credential patterns, rejects local secret/config files, validates local image paths, and rejects external image hosts in the README.
