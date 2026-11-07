# Shovo127 profile repository — setup and maintenance

## Core principles

- Keep the repository public; it is the account's profile README repository.
- All README images are stored in this repository and referenced with relative paths.
- Never commit personal tokens, API keys or private account data.
- The default workflows use GitHub's built-in GITHUB_TOKEN and repository-owned scripts.
- A metric must be traceable to a public source. Unavailable data must stay unavailable, not be fabricated.

## Workflows

| Workflow | Purpose | Trigger |
|---|---|---|
| profile-dashboard.yml | Refresh dashboard SVG/PNG/JSON, live contribution calendar, metrics city, data-driven snake GIF and asset inventory | Daily schedule, generator or contribution-data changes, manual |
| profile-assets.yml | Snapshot contribution data, render and validate all Blender scenes, refresh snake/metrics media and update the asset inventory | Renderer/packer/contribution-data generator changes, manual |
| profile-3d.yml | Manual 3D render entry point | Manual |
| readme-check.yml | Validate local image references, SVGs, dashboard/contribution JSON, all asset metadata, scripts and public leaks | PR, successful media workflow, manual |
| snake.yml | Verify the preserved classic snake GIF | Manual |
| blog-post-workflow.yml | Update latest posts from a user-supplied RSS/Atom feed | Daily schedule/manual, only if BLOG_FEED_URL is configured |

The old duplicate metrics.yml workflow has been removed; profile-dashboard.yml is the single dashboard entry point.

## Permissions and secrets

No additional secret is required for the standard public dashboard and rendering pipeline. GitHub Actions supplies GITHUB_TOKEN automatically. Keep workflow permissions limited to contents: read or contents: write as declared in each workflow.

Optional integrations:
- PROFILE_READ_TOKEN: optional classic GitHub personal access token with only the read:user scope. The workflow first uses its built-in GITHUB_TOKEN to request public contribution data. Add PROFILE_READ_TOKEN as a repository Actions secret only if you want GitHub to include private/internal contribution counts. It does not need repository write access; GITHUB_TOKEN handles repository commits. To include private counts, also enable the GitHub profile setting that displays private contribution counts. GitHub's GraphQL documentation notes that private/internal contribution records require read:user scope. If GitHub rejects the available token, the city is rendered as a neutral empty calendar and no counts are invented.
- BLOG_FEED_URL: repository variable containing an RSS/Atom feed URL that belongs to you. Without it, the blog updater is dormant.
- WAKATIME_API_KEY, Spotify, Discord and LeetCode credentials: not implemented; do not add secrets for them until the integration has a verified data source and a repository-owned generator.

Never paste credentials into this document, README, issue, workflow log or commit.

## Run manually

1. Open the repository's Actions tab.
2. Select the workflow by its name.
3. Choose Run workflow.
4. Review the run logs and verify the generated files before accepting any README media changes.

## 3D asset generation

- scripts/render_profile_3d.py builds original Blender geometry, materials, lighting, camera framing and eased animation.
- scripts/pack_profile_3d.py uses Pillow to create shared-palette animated GIFs. scripts/generate_contribution_snake.py simulates a collision-free route through the actual 53-week calendar, places food only on days with recorded contributions, and grows the snake as it reaches those days.
- Blender is downloaded from the official Blender release server and checked against the published SHA-256 checksum.
- Intermediate PNG frames are temporary runner files; committed GIFs live in assets/3d/.
- Current scene outputs are 900×225, 10 frames, 120 ms per frame, with matching first/last poses for seamless infinite looping.
- The profile build renders all 12 selected Blender scenes at six Eevee TAA samples. All 12 outputs are self-hosted in assets/3d/; the approved classic contribution snake remains preserved separately from the new data-driven snake.
- Rendering uses Eevee Next with software rendering on GitHub-hosted Linux runners. The first verified twelve-scene render took about 6 minutes from job start through commit. The final render adds camera dolly/orbit movement and a warm rim-light sweep; actual duration varies with runner load.
- The profile workflow promotes the new scene GIFs only after every expected output passes validation.

The contribution city is built from the GitHub GraphQL contributionCalendar. scripts/fetch_contribution_data.py writes assets/contribution-calendar.json and assets/contribution-city-data.svg. Before rendering, profile-assets.yml copies that dated data to assets/contribution-city-source.json; Blender reads this immutable render snapshot to build the 3D isometric calendar city. The daily dashboard refresh may update the live calendar, static SVG and snake without silently changing the data snapshot behind the 3D GIF. scripts/generate_metrics_city.py writes assets/metrics-city.svg from the public repository metrics, language byte totals, verified project categories and contribution total when available. If PROFILE_READ_TOKEN and the built-in GITHUB_TOKEN are both absent or rejected, the JSON records status=unavailable and the city uses a neutral empty grid. The built-in token may provide public contribution data; PROFILE_READ_TOKEN is optional for read:user/private contribution visibility. It never invents activity. Private counts appear only when the account setting and token scope permit them.

## Dashboard data

scripts/generate_dashboard.py calls the GitHub public REST API and writes:
- assets/github-dashboard.svg
- assets/github-dashboard.png
- assets/github-dashboard-data.json
- assets/metrics-city.svg — generated from the same verified public metrics, repository language bytes, project categories and contribution data when available.
- assets/contribution-calendar.json — latest daily contribution data.
- assets/contribution-city-source.json — exact contribution data snapshot used by the current 3D city GIF.
- assets/contribution-city-data.svg — static city from the latest contribution data.
- assets/contribution-snake-live.gif — generated from the same daily counts; not a playable game.

The dashboard JSON records the source, UTC generation timestamp, public account metrics, language byte totals and public repository metadata. Language shares are code volume across non-fork, non-archived public repositories; they are not skill scores. If a language API request fails, generation fails rather than silently publishing a partial distribution.

## Asset inventory

- docs/profile-audit/asset-inventory.json and asset-inventory.md record every file under assets/, including exact dimensions, animation frame counts, frame timing, loop flags, file sizes and SHA-256 hashes.
- scripts/audit_profile_assets.py regenerates the inventory deterministically. The README validation workflow runs it in --check mode to catch stale metadata.

## Optional blog feed

Set the repository variable BLOG_FEED_URL to an RSS or Atom feed you own. Remove or clear the variable to disable the integration. The script only accepts public HTTP(S) links from feed entries and leaves the README unchanged when no valid entries are returned.

## Asset and profile maintenance

- Keep existing approved assets unless a replacement has passed visual and technical checks.
- Use descriptive alt text and avoid excessive full-width motion.
- GitHub README cannot run arbitrary JavaScript; a GIF is not an interactive game.
- The snake.yml workflow verifies the preserved classic GIF; the daily profile-dashboard.yml workflow generates the data-driven contribution-snake-live.gif.
- The contribution-city generator uses GITHUB_TOKEN for public data; PROFILE_READ_TOKEN is optional for private counts. If GitHub GraphQL data is unavailable, the neutral empty state is intentional.
- scripts/audit_profile_assets.py regenerates the deterministic asset inventory; readme-check.yml runs it in --check mode to catch stale metadata.
- Check the generated JSON and workflow run before trusting dashboard values.
- See assets/design-system.md and docs/profile-audit/ for design and audit decisions.
