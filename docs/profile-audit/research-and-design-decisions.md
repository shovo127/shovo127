# Research and design decisions — 2026-11-07

## Platform constraints

GitHub renders a profile README as Markdown with supported HTML and images. It does not execute arbitrary JavaScript in the README. The profile README must be in a public repository whose name matches the account username. See:
- https://docs.github.com/en/account-and-profile/concepts/personal-profile
- https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

## Reference project review

| Reference | Useful concept | Self-hosting and limitations | Decision |
|---|---|---|---|
| ayyazzafar | Profile storytelling and visual hierarchy | Design reference, not a dependency | Study layout; do not clone |
| github-readme-activity-graph | Activity chart as a compact visual | Common embed is a hosted image endpoint; local generator is preferable | Do not embed hosted output |
| github-profile-trophy | Achievement-oriented summary | Common usage depends on hosted renderer; trophy claims require verification | No remote image or unsupported trophy claims |
| github-profile-3d-contrib | Isometric contribution calendar | Workflow-generated files can be committed locally; contribution data must be verified | Reference for a future data-backed city |
| lowlighter/metrics | Broad plugin architecture and local SVG output | Supports GitHub Actions and self-hosted setup; plugins may require extra scopes or credentials; project documents MIT licensing | Do not adopt wholesale; use a focused local subset |
| Platane/snk | Contribution-grid path rendered as snake GIF/SVG | Data-driven action; verify licence and source behaviour before copying code | Preserve approved GIF; no unlicensed source reuse |
| athul/waka-readme | WakaTime coding activity integration | Requires a real WakaTime account and API key | Optional only after credentials and consent |
| gautamkrishnar/blog-post-workflow | RSS/Atom-to-README updates | Third-party action is unnecessary; local RSS parser already exists | Keep repository-owned updater and explicit feed URL |
| DenverCoder1/readme-typing-svg | Typing animation as a hero accent | Typical embeds use a remote SVG service | Not adopted |
| anuraghazra/github-readme-stats | Compact stats-card information architecture | Public hosted endpoint may be rate-limited; project documents GitHub Actions/static self-hosting | Keep local dashboard generator and improve data handling |

## Adopted implementation decisions

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
