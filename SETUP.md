# Profile repository maintenance

The public profile README uses repository-owned media. Displayed animations are committed under `assets/`; the README does not depend on remote image hosts, animation services or icon CDNs.

## 3D rendering pipeline

- `.github/workflows/profile-assets.yml` builds the profile media automatically when the README or Blender scene scripts change.
- `scripts/render_profile_3d.py` renders the product scenes with **Blender**, an open-source 3D renderer.
- `scripts/pack_profile_3d.py` converts the rendered frames into self-hosted animated GIFs.
- The resulting 3D animations are stored in `assets/3d/` and embedded directly in the README.
- The previously approved `assets/section-08-contribution-snake.gif` is restored byte-for-byte from its earlier repository revision. The snake workflow only verifies it; it does not regenerate or replace it.
- `.github/workflows/readme-check.yml` validates local image references, media file signatures, SVG integrity, Python syntax and workflow declarations.

The rendering workflow downloads the official Blender 4.5.15 Linux archive, verifies it against Blender's published SHA-256 checksum, and uses Pillow to package the rendered frames. GitHub Actions' built-in `GITHUB_TOKEN` is limited to repository contents. No personal access token, paid image service or third-party GitHub Action is required.

## Other repository-owned media

- `.github/workflows/profile-dashboard.yml` builds the GitHub dashboard from public repository data.
- `scripts/generate_dashboard.py` generates the dashboard SVG; a PNG copy is used for README compatibility.
- `scripts/update_blog_feed.py` updates the writing section only when the optional `BLOG_FEED_URL` repository variable is configured.
- Previous SVG artwork and earlier GIF iterations remain in `assets/` as preserved source/history; the current README uses the new 3D renders for its main visual sections.

## Security and maintenance

- Never put credentials, private keys, recovery codes, personal access tokens or private data in README files, SVGs, GIFs, workflow logs or commits.
- Do not add third-party image URLs to README `img`, `source` or Markdown image syntax. Add media to `assets/` and reference it with a relative path.
- Keep workflow permissions minimal. Rendering and dashboard workflows need `contents: write`; validation needs only `contents: read`.
- Prefer repository-owned scripts and GitHub's built-in token over third-party actions.
- Contribution data must come from GitHub's public contribution calendar. If the data source is unavailable, do not invent contribution totals.

## Motion and accessibility

Animations are decorative and do not carry essential information. Keep motion subtle, slow, non-flashing and lightweight. GitHub profile README rendering does not provide a reliable custom pause control or a CSS `prefers-reduced-motion` switch for embedded GIFs, so avoid intense or large-area motion. Keep descriptive alt text.

## Repository visibility

This repository must remain public for GitHub to display it as a public profile README. Do not store secrets here. GitHub Actions secrets and variables belong in repository Settings and must never be copied into tracked files.
