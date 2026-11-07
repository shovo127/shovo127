# Profile repository — setup and maintenance

## Purpose

This username-matching repository powers the public GitHub profile README. The README is an engineering and software portfolio; all supporting artwork is self-hosted here. The opening Hero is approved and immutable unless the owner explicitly requests a future change.

## Structure

- README.md — profile content and project showcase.
- assets/hero/engineering-hero.svg — approved Hero; protected by the validation workflow.
- assets/projects/ — five original project-specific interface/architecture studies.
- assets/engineering/ — original 3D mechanical render, technical focus and education visuals.
- assets/motion/signal-sweep.gif — one restrained 24-frame, 5.28-second ambient loop.
- assets/data/public-repositories.json — dated public GitHub metrics snapshot.
- assets/data/public-repository-snapshot.jpg — visualisation of the same snapshot.
- tools/render_portfolio_art.py — reproducible local artwork generator (Python + Pillow).
- scripts/check_public_leaks.py — common high-confidence credential-pattern and forbidden-filename checks.
- scripts/validate_profile_readme.py — Hero lock, local references, image dimensions, GIF properties, SVG validity and asset budget.
- scripts/update_blog_feed.py — optional RSS/Atom list updater, activated only by BLOG_FEED_URL.
- tests/ — standard-library tests for the optional feed updater.
- docs/design/cyberpunk-system.md — visual and motion rules.
- docs/profile-audit/cyberpunk-redesign.md — evidence, scope and known rendering limitations.

## Generate artwork locally

Use Python 3.11+ and Pillow:

```bash
python -m pip install Pillow==11.3.0
python tools/render_portfolio_art.py
```

The generator has no network calls and uses only project-specific vector/raster drawing plus a small parametric triangle-mesh renderer for the piston, connecting rod and crankshaft study. It writes generated artwork to `assets/` and records the public repository snapshot in JSON.

The source script and generated outputs are committed together. Do not manually edit generated outputs; update the generator and rerun it instead.

## Workflows

| Workflow | Purpose | Trigger |
|---|---|---|
| Validate profile README | Public secret-pattern scan, feed updater tests, Hero lock, local references, image/GIF integrity and asset budget | Push to main, pull request to main, manual |
| Render portfolio assets | Reproducibly regenerate self-hosted artwork and commit changed outputs | Push to the cyberpunk redesign branch, manual |

The validation workflow uses `actions/checkout@v7`, Python and Pillow. It needs only `contents: read`. The rendering workflow uses the built-in `GITHUB_TOKEN` with `contents: write` on the dedicated redesign branch only. No personal access token or third-party API key is required.

## Optional blog feed

Set the repository variable `BLOG_FEED_URL` to a public RSS or Atom feed URL that belongs to you. The separate blog workflow is dormant when the variable is empty. When enabled, it fetches at most 2 MiB, accepts only HTTP(S) post links, selects up to five newest valid entries and inserts or updates a compact “Latest writing” section immediately before Connect. If no valid entries are returned, the README is left unchanged.

The updater uses only the Python standard library and is covered by automated tests. Clear `BLOG_FEED_URL` to disable the integration.

## Analytics snapshot

The current snapshot is dated 2026-11-07. It covers seven public project repositories, excludes the profile repository and private repositories, and records repository stars, forks and GitHub-reported primary language. Language counts are repository counts, not code-byte percentages or skill ratings. The snapshot is intentionally dated; it is not a live counter.

## Security

- Never commit API keys, access tokens, passwords, cookies, private keys, certificates, recovery codes, private user information or unredacted diagnostic logs.
- Keep environment files, credential exports and key stores out of Git.
- The public leak scanner detects common high-confidence credential patterns and forbidden secret filenames; it cannot guarantee detection of every possible secret.
- The optional feed updater uses the built-in token. No personal access token is required.
- Keep workflow permissions at the minimum needed.

## GitHub rendering limits

- The approved Hero source and opening README block are protected by exact checks.
- GitHub profile READMEs do not provide arbitrary custom CSS, JavaScript, event handlers or guaranteed SVG SMIL playback. The README therefore uses ordinary Markdown/HTML and self-hosted JPEG/GIF/SVG assets.
- GIFs are visual loops, not interactive controls. The animated sweep is 560×84, 24 frames at 220 ms per frame.
- GitHub controls the page background/theme, native contribution graph, activity timeline and pinned repository cards. The README cannot force the whole profile background to pure black or restyle native profile components.
- Actual live desktop/mobile/theme rendering and GIF playback must be visually checked on GitHub; local browser rendering and source validation are not substitutes for that check.
