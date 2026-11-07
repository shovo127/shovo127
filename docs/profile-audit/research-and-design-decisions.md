# Research and design decisions — 2026-11-07

## Platform constraints

GitHub renders a profile README as Markdown with supported HTML and images. It does not execute arbitrary JavaScript in the README. The profile README must be in a public repository whose name matches the account username. See:
- https://docs.github.com/en/account-and-profile/concepts/personal-profile
- https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

## Reference project review

| Reference | Useful concept | Self-hosting and limitations | Decision |
|---|---|---|---|
| ayyazzafar | Profile storytelling and visual hierarchy | Design reference, not a dependency | Study layout; do not clone |
| github-readme-activity-graph | Activity chart as a compact visual | MIT; public deployment moved to Vercel, with a documented self-deploy route. Last pushed 2026-05-17. Hosted embed adds a runtime dependency. | Do not embed hosted output; local data snapshot is preferable |
| github-profile-trophy | Achievement-oriented summary | MIT; repo was pushed 2026-10-27. README documents a Deno renderer, CI generation and Vercel self-hosting; upstream owner has raised hosting-cost concerns. | Do not add until verified achievement definitions and local generator are tested |
| github-profile-3d-contrib | Isometric contribution calendar | MIT; pushed 2026-11-05. Action generates SVGs using GitHub contribution data; depends on a working token and GitHub Actions. | Reference for a future data-backed city; do not substitute for actual data validation |
| lowlighter/metrics | Broad plugin architecture and local SVG output | MIT; pushed 2026-05-29. Supports GitHub Actions, CLI and self-hosted deployment; plugins may require extra scopes, API calls or credentials. | Do not adopt wholesale; current repository-owned dashboard is smaller and easier to audit |
| Platane/snk | Contribution-grid path rendered as snake GIF/SVG | Repo pushed 2026-10-18; GitHub API reports no SPDX licence. Do not copy or redistribute its source without permission. | Preserve approved GIF; no source-code reuse |
| athul/waka-readme | WakaTime coding activity integration | MIT; pushed 2026-10-23. Requires a real WakaTime/Wakapi API key; generated time/language totals reflect that service's recorded usage. | Optional only after credentials and consent |
| gautamkrishnar/blog-post-workflow | RSS/Atom-to-README updates | AGPL-3.0; pushed 2026-10-07. Supports many RSS/Atom sources and configurable templates; using it as an Action adds an external dependency. | Keep repository-owned updater and explicit feed URL |
| DenverCoder1/readme-typing-svg | Typing animation as a hero accent | MIT; pushed 2026-11-05. Supports PHP self-hosting, but typical embeds use a remote SVG service. | Not adopted; original static/Blender hero has more identity |
| anuraghazra/github-readme-stats | Compact stats-card information architecture | MIT; pushed 2026-10-01. Public Vercel endpoint warns about rate limits; repository documents GitHub Actions/static self-hosting. | Keep local dashboard generator and improve data handling |

## Research snapshot and licensing\n\nRepository metadata was checked through GitHub on 2026-11-07. Snapshot: activity-graph MIT (last push 2026-05-17); profile-trophy MIT (2026-10-27); profile-3d-contrib MIT (2026-11-05); metrics MIT (2026-05-29); snk has no SPDX licence listed (2026-10-18); waka-readme MIT (2026-10-23); blog-post-workflow AGPL-3.0 (2026-10-07); readme-typing-svg MIT (2026-11-05); github-readme-stats MIT (2026-10-01). The ayyazzafar reference repository has no SPDX licence listed and is used only as a visual reference. Push dates indicate repository activity, not a formal maintenance guarantee.\n\n## Adopted implementation decisions

1. Repository-owned media: all primary README images stay in this repository with relative paths.
2. Blender over remote animation generators: use Blender's official binary with checksum verification and local Pillow packaging. It is slower than static vector art but creates reproducible 3D scenes.
3. No third-party Actions by default: workflows use shell, Python and GitHub's built-in token. This reduces supply-chain surface but requires maintaining scripts directly.
4. One dashboard source of truth: use public REST API data and local SVG/PNG generation. Clearly label repository counts, stars and language byte shares.
5. No fake achievements: do not render trophy claims without a source that confirms them.
6. Contribution data is a separate engineering requirement: decorative Blender towers are not contribution data. A city must not be published as contribution analytics until actual contribution counts and dates are acquired and checked.
7. WakaTime, Spotify, Discord, RSS and LeetCode remain opt-in until an authentic source and required permissions are configured.

## External research notes

- GitHub's official profile docs confirm that README content, profile activity, achievements and public profile visibility are separate profile features.
- lowlighter/metrics documents GitHub Actions, a self-hosted deployment option, many plugins (including achievements, activity, isocalendar, repositories, RSS and WakaTime), and an MIT licence.
- Platane/snk describes a contribution-calendar-to-snake GIF/SVG workflow. The existing repository asset is preserved rather than copying code from a project whose licence must be checked independently.
- anuraghazra/github-readme-stats warns that its public Vercel endpoint can be unreliable and documents GitHub Actions/static self-hosting as an alternative.
- github-profile-3d-contrib generates a 3D contribution-calendar image and is a useful visual reference, but does not replace checking which contribution data is accessible.

## Sources

- https://docs.github.com/en/account-and-profile/concepts/personal-profile
- https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
- https://github.com/lowlighter/metrics
- https://github.com/Platane/snk
- https://github.com/yoshi389111/github-profile-3d-contrib
- https://github.com/anuraghazra/github-readme-stats
- https://github.com/ashutosh00710/github-readme-activity-graph
- https://github.com/ryo-ma/github-profile-trophy
- https://github.com/athul/waka-readme
- https://github.com/gautamkrishnar/blog-post-workflow
- https://github.com/DenverCoder1/readme-typing-svg
- https://github.com/ayyazzafar
