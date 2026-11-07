# Profile repository — setup and maintenance

## Repository purpose

This is the public profile repository for the GitHub account. Its README is a concise engineering and software portfolio. The approved Hero is protected by automated checks; project visuals are self-hosted SVG diagrams.

## Current repository structure

- README.md — profile content and project showcase.
- assets/hero/ — approved Hero artwork (do not modify without explicit approval).
- assets/motion/ — restrained section divider.
- assets/projects/ — five project-specific schematic illustrations.
- docs/design/motion-system.md — visual, motion and compatibility rules.
- docs/profile-audit/phase-2.md — evidence and known platform limitations.
- scripts/check_public_leaks.py — high-confidence credential-pattern and forbidden-filename checks.
- scripts/validate_profile_readme.py — Hero lock, local references, SVG validity and asset budgets.
- scripts/update_blog_feed.py — optional RSS/Atom list updater, activated only by BLOG_FEED_URL.
- tests/ — standard-library tests for the feed updater.

## Workflows

| Workflow | Purpose | Trigger |
|---|---|---|
| Validate profile README | Secret-pattern scan, feed updater tests, Hero lock, local image/link paths, SVG parsing and asset budget | Push, pull request, manual |
| Update latest blog posts | Optional RSS/Atom feed update; runs only when BLOG_FEED_URL is configured | Daily schedule, manual |

The validation workflow uses actions/checkout v7 (Node.js 24 runtime) and only contents: read. The optional feed workflow needs contents: write to commit its generated README change. Both use GitHub's built-in GITHUB_TOKEN; no personal access token or API secret is required.

## Optional blog feed

Set the repository variable BLOG_FEED_URL to a public RSS or Atom feed URL that belongs to you. The workflow is dormant when the variable is empty. When enabled, it fetches at most 2 MiB, accepts only HTTP(S) post links, selects up to five newest valid entries and inserts or updates a compact “Latest writing” section immediately before Connect. If no valid entries are returned, the README is left unchanged.

The updater uses only the Python standard library. Its RSS/Atom parsing and README insertion behaviour are covered by automated unit tests. Clear BLOG_FEED_URL to disable the integration.

## Security

- Never commit API keys, access tokens, passwords, cookies, private keys, certificates, recovery codes, private user information or unredacted diagnostic logs.
- Keep environment files, credential exports and key stores out of Git.
- scripts/check_public_leaks.py checks tracked files for common high-confidence credential patterns and forbidden secret filenames. It is a safeguard, not a guarantee that every possible secret can be detected.
- Use GitHub Actions secrets only when an integration genuinely requires a credential. Do not add secrets for unimplemented integrations.
- Keep workflow permissions at the minimum needed.

## Design and compatibility

- Keep all README images self-hosted and use case-correct relative paths.
- Preserve the approved Hero and its asset; CI fails if the opening block or Hero SVG changes.
- Do not add custom CSS, JavaScript, remote image widgets or unverified metrics.
- GitHub owns the native contribution graph, activity timeline and pinned repository cards.
- SVG motion playback, narrow-screen table behaviour and theme rendering require visual inspection on GitHub; source validation does not prove browser rendering.
- See docs/design/motion-system.md and docs/profile-audit/phase-2.md for the current system and known limitations.
