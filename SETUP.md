# Profile repository maintenance

The public profile README is intentionally self-contained: every displayed image and illustration is stored in this repository under `assets/`. The README does not load images from badge services, icon CDNs, statistics providers, or third-party image hosts.

## Automated media

- `.github/workflows/profile-assets.yml` runs the local generator in `scripts/generate_profile_media.py`.
- The generator creates the subtle animated GIFs and contribution snake, then commits them into `assets/`.
- `.github/workflows/profile-dashboard.yml` builds the GitHub dashboard SVG from GitHub's public API and commits it into `assets/`.
- `.github/workflows/readme-check.yml` verifies that every displayed image is repository-local, all required media exists, and the generator compiles.

These workflows use GitHub Actions' built-in `GITHUB_TOKEN` with repository-scoped permissions. No personal access token, API key, WakaTime key, Spotify token, Discord bot token, or other private credential is required for the core profile.

## Current implementation\n\nThe README currently uses only repository-local image files. Ten subtle section-level GIF animations plus the contribution snake are generated into `assets/`; all static profile illustrations are also checked into the same folder. The dashboard is generated locally as SVG. No remote image badge, icon CDN, statistics image provider, or animation host is used.\n\n## Security and maintenance

- Never put credentials, private keys, recovery codes, personal access tokens, or private data in README files, SVGs, GIFs, workflow logs, or commits.
- Do not add third-party image URLs to README `img`, `source`, or Markdown image syntax. Add the image to `assets/` and reference it with a relative path.
- Keep workflow permissions minimal. The media and dashboard workflows need `contents: write`; the README validator needs only `contents: read`.
- Review workflow changes before merging. Prefer repository-owned scripts and GitHub's built-in token over third-party actions.
- The contribution snake uses public contribution-calendar data when available. If GitHub's API does not provide it, the contribution grid stays neutral rather than fabricating contribution totals.

## Motion and accessibility

Animations are decorative and do not carry essential information. Keep them slow, low-contrast, non-flashing and lightweight. GitHub profile README rendering does not provide a reliable custom pause control or a CSS `prefers-reduced-motion` switch for embedded GIFs, so avoid intense or large-area motion. Keep descriptive alt text and a static illustration beside animated media.

## Repository visibility

This repository must remain public for GitHub to display it as a public profile README. Do not store secrets here. GitHub Actions secrets and variables belong in repository Settings and must never be copied into tracked files. Branch protection and ruleset configuration should be managed in GitHub repository settings by an administrator; the connected integration used for this maintenance cannot read or change those administrative settings.
