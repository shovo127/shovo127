# Profile redesign — Phase 2 audit record

## Scope and protection

- Repository: shovo127/shovo127, default branch main.
- Working branch: redesign/phase-2-profile-sections.
- Pre-Phase-2 main commit: 398f2047ef182ae3832d5ce9120307cb35b6e481.
- The approved Hero is the opening README block: hero image, name, positioning line and contact links, through the first horizontal divider.
- Hero source asset assets/hero/engineering-hero.svg was not edited.
- CI locks both the exact README Hero block and the Hero SVG Git blob SHA.

## Public project evidence reviewed

- VisaFlowX Universal README: Manifest V3, site profiles, DOM monitoring, rules, retries, scheduling, notifications and manual protected verification.
- Kostenlos AI README: React, TypeScript, Tailwind CSS, Appwrite, Cloudflare Pages; bring-your-own-key provider failover and optional Tavily context.
- Noti-Fixer README: Python scripts and ADB workflow; Android ROM-specific notification diagnostics and reversible settings with user approval.
- Circle to Search for Xiaomi README: native Android trigger, HyperOS Back Tap and Google device-eligibility boundaries.
- Smart Scanner Pro README and architecture document: Windows / .NET 9 / WPF architecture. Its feature section is explicitly labelled planned; the profile copy preserves that distinction.

## README and asset changes

- Selected Work uses five self-hosted, project-specific schematic illustrations and concise repository-grounded descriptions.
- Technical focus, Education, Connect and footer use a consistent editorial hierarchy.
- No demo URL, user count, downloads, performance figure, contribution total or proficiency percentage was added.
- No separate contribution chart was added because GitHub's native contribution graph and activity feed are the authoritative display; duplicating them would add unverified or redundant data.
- No new 3D render was added: the project-specific schematics explain the actual software workflows more directly than decorative machinery.
- No files were removed in Phase 2.

## Native GitHub interface boundaries

- Pinned repository cards and contribution graph are account/profile UI, not README-controlled content.
- No authorized pinned-repository mutation action was available; native pin order was not changed.
- Public profile HTML could not be retrieved through the available GitHub/web interface, so the current pinned order and live graph appearance were not independently verified.
- The four user-referenced screenshots were not exposed as readable image attachments in the conversation context. Screenshot-by-screenshot comparison remains unverified.

## Rendering and verification boundaries

- CI locks the Hero, checks local references, parses SVGs, rejects embedded active content and remote SVG dependencies, and enforces asset budgets.
- All README images resolve to self-hosted repository files; total asset size is 17,086 bytes.
- GitHub desktop/mobile rendering, dark/light theme appearance, table wrapping and SVG SMIL playback still require browser-level visual QA. Passing CI is not evidence of those visual behaviours.

## Follow-up maintenance

- The existing optional blog workflow referenced a missing scripts/update_blog_feed.py file. The updater and standard-library tests were restored without changing its opt-in behaviour.
- CI now runs the existing public-leak scanner and the feed updater tests.
- The workflow uses actions/checkout v7 (Node.js 24 runtime), removing the Node.js 20 deprecation warning seen in the initial Phase 2 run.
