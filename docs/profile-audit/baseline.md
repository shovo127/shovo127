# Baseline audit — 2026-11-07

## Scope and recovery point

- Repository: https://github.com/shovo127/shovo127
- Audited branch: main
- Audited starting commit: 8e04c00f57c8f4aa3f9a86c5a17e5bc010b99888
- Recovery branch created before implementation: backup/profile-before-master-rebuild-2026-11-07
- Audit covered the recursive Git tree, README, workflows, generation scripts, recent history and available public repository metadata.

## Existing profile features

- Centered hero and identity statement.
- Education, German learning, technology interests and project links.
- Local GitHub dashboard in SVG and PNG.
- Twelve numbered section GIFs, a restored contribution snake, additional motion GIFs, SVG illustrations and project cards.
- Repository-owned Blender renderer and Pillow GIF packer.
- Dashboard, media, blog-feed, snake and validation workflows.
- Optional RSS/Atom workflow, dormant until BLOG_FEED_URL is configured.

## Assets worth preserving

- assets/banner.svg and assets/section-01.gif through assets/section-12.gif.
- assets/section-08-contribution-snake.gif: restored byte-for-byte from its previously approved historical revision; its blob SHA was compared with the historical blob.
- assets/github-dashboard.svg and assets/github-dashboard.png.
- Additional motion GIFs: about, achievement, beyond-code, city, connect, dashboard, focus, habits, profile, projects and technology.
- Existing SVG illustrations and project cards under assets/ and assets/projects/.

No existing asset was deleted during this audit.

## Existing automation

- profile-dashboard.yml: scheduled public GitHub REST API dashboard generation.
- profile-assets.yml: Blender render, GIF packaging and guarded README switch.
- profile-3d.yml: manual 3D render entry point.
- readme-check.yml: README media, SVG, syntax and security checks.
- snake.yml: verifies the preserved snake; it does not generate a new snake.
- blog-post-workflow.yml: optional RSS/Atom feed updater.
- metrics.yml: legacy manual dashboard refresh overlapping the scheduled dashboard workflow.

Inspected workflows use repository-owned scripts rather than third-party GitHub Actions. They use the built-in GITHUB_TOKEN; no personal token is hardcoded.

## Defects and risks found

1. 3D validation mismatch: the renderer and packer generated 900×225, 10-frame GIFs, but the failed run's validation expected 960×240, 12 frames. Blender rendering and GIF packaging succeeded; the stale assertion caused the workflow failure and blocked publishing.
2. Timeout margin: software Eevee rendering took about 6 minutes 34 seconds for twelve scenes, before setup and validation overhead. An eight-minute job timeout was too tight.
3. Contribution city is not data-driven: the Blender city scene creates six decorative towers. It is not derived from GitHub contribution counts and must not be described as contribution analytics.
4. Contribution snake automation: snake.yml only verifies the restored GIF. It does not regenerate contribution data or animation. README wording must not imply that this workflow regenerates it.
5. Dashboard completeness: the generator fetches up to 100 repositories and requests language totals individually. Language-request exceptions are silently ignored, which can make an incomplete language distribution look complete.
6. Duplicate workflow: metrics.yml repeats dashboard generation already handled by profile-dashboard.yml.
7. Featured project descriptions: the README has few project descriptions and does not clearly distinguish public repositories from private projects or experiments.
8. Documentation gaps: the requested audit, design, implementation and verification reports and an asset-generation source guide were absent.
9. Asset quality evidence: dimensions, animation counts and byte sizes are not centrally inventoried. Visual review is required before promoting every new render.
10. Contribution-data access: public REST repository endpoints do not provide the complete contribution calendar. Private contribution visibility cannot be assumed.

## Design weaknesses

- Repeated full-width motion banners create substantial vertical length and compete with project descriptions.
- Several headings imply achievements or contribution data without a matching data source.
- Featured work is text-only and under-explained.
- The profile needs stronger separation between confirmed education, active learning, exploratory interests and shipped projects.
- The Blender scenes use a consistent product-studio visual language, but are not all appropriate as contribution analytics.

## Data accuracy risks

- Repository language byte counts are not proficiency scores.
- Public repository count, public stars, followers and following need clear definitions.
- API failures must be surfaced as unavailable or incomplete, not silently converted into zero or partial totals.
- Contribution totals and private activity must not be fabricated.
- No coding hours, revenue, adoption, rankings or awards should be inferred.

## Features to preserve

- Approved contribution snake file and original bytes.
- Existing local dashboard and public-API-only approach, after correcting failure handling.
- Original SVG illustrations, project cards and section animations until replacements are verified.
- Repository-owned Blender pipeline, after correcting its validation contract and publishing only validated outputs.
- Optional RSS integration as opt-in.

## Features requiring correction

- Stale 3D validation expectations.
- Decorative city scene's misleading contribution label.
- Dashboard error handling and repository pagination/completeness reporting.
- Redundant workflow entry point and unclear automation documentation.
- README storytelling and project descriptions where evidence is available.

## Baseline conclusion

The repository already contains meaningful custom artwork and automation. The latest render failure was a validation-contract defect, not a Blender render failure. New 3D output must remain unpublished until corrected checks pass and the files are inspected. Contribution analytics must remain explicitly unavailable until a reliable, documented data source is implemented.
