# Black and blood-red engineering portfolio — implementation audit

## Baseline and rollback

- Repository: `shovo127/shovo127`.
- Main baseline: `3db0c4944ac663560bfd246f66c1a63babbe878f`.
- Rollback branch: `backup/pre-blood-red-redesign-2026-11-07`.
- Implementation branch: `redesign/blood-red-engineering-portfolio`.
- Approved Hero README opening block was recorded before edits.
- Approved Hero SVG blob SHA: `f988a3193de32412396a760fee2cf46d7de771e4`.

## Initial findings and root causes

The previous profile was not aligned with the new brief:
- The design documentation and generated assets used a cyan/teal-led palette with violet/magenta/lime accents.
- The project section used static interface studies, and the sixth IPTV project had no project artwork.
- Technical Focus used plain table text and one composite image rather than six separate discipline cards.
- The page reused one small 24-frame/220 ms cyan sweep three times. Project art, technical cards and analytics had no dedicated motion treatments.
- The validator enforced fixed image dimensions, 150 KiB per asset, 800 KiB total, exact 24-frame/220 ms GIF metadata, fixed project image counts and fixed table-width assumptions. These constraints encoded the previous artwork implementation, not reusable security requirements.

## Implementation

- Recoloured the generated portfolio artwork into a black, deep-charcoal and blood-red palette.
- Created six separate 640×300 Technical Focus card images.
- Added IPTV By Shovo artwork based on the public playlist repository.
- Created six project-specific animated scan GIFs from each project's generated visual study.
- Added separate section sweep, Technical Focus pulse and analytics trace GIFs.
- Re-rendered the existing parametric piston/connecting-rod/crankshaft mesh study in the revised palette; no unrelated machinery or source CAD model was introduced.
- Re-rendered the education timeline and dated public repository analytics chart.
- Replaced the README project layout with six two-column project cards, six distinct Technical Focus cards, the engineering study, education, analytics, Connect and animated footer.
- All key descriptions, stacks, safety boundaries, planned-feature qualifications and links remain readable HTML text rather than rasterised artwork.

## Project-source verification

- VisaFlowX Universal README: Manifest V3 browser workflow assistant, profile-driven rules, DOM monitoring, retry/backoff, scheduling and notifications. Protected verification is explicitly user-completed; bypass behaviour is prohibited.
- Kostenlos AI README: React/TypeScript BYOK chat app, Appwrite-managed provider keys, Groq/Gemini/OpenAI/Mistral failover and optional Tavily context.
- Noti-Fixer README: Python/ADB wireless pairing, diagnostics and proposed changes requiring explicit user review/approval; claims are kept bounded to documented workflows.
- Circle to Search README: Xiaomi/HyperOS double-back-tap trigger invoking Google's native surface through Android Voice Interaction Manager; Google default-assistant and device eligibility remain constraints.
- Smart Scanner Pro README is at `SmartScan/README.md` (not repository root). It documents C#/.NET 9 Windows architecture and Clean Architecture; TWAIN/WIA/eSCL, OCR, duplex, plugin and related features are explicitly marked planned.
- IPTV By Shovo README: public third-party channel links and M3U/M3U8 playlist collection; no video streams are hosted by this repository.

## Analytics

Source: `assets/data/public-repositories.json`, captured from GitHub public repository metadata on 2026-11-07. Scope excludes the profile repository and private repositories.

- Seven public project repositories.
- Thirteen stars and four forks.
- Primary-language repository labels: JavaScript 2, TypeScript 2, C# 1, PowerShell 1, Python 1.
- Counts are dated static values. The analytics GIF is a decorative signal trace and does not change the data.

## Validation changes

Removed obsolete assumptions:
- Fixed old raster dimensions for every image.
- 150 KiB per-raster limit and 800 KiB total asset limit.
- Exact 24-frame/220 ms GIF rule.
- Previous exact project image count and HTML table-width counts.

Replaced them with:
- Exact Hero README block and SVG Git blob lock.
- Local image/link resolution and rejection of remote image dependencies.
- SVG XML, script, foreignObject and remote-reference checks.
- Expected image formats and intended dimensions.
- Nine animated GIF checks: expected dimensions, animation, infinite loop, frame timing and total loop duration.
- Six distinct project card and six distinct Technical Focus asset references.
- 300 KiB static raster, 350 KiB GIF and 3 MiB total asset budgets.
- Existing public-secret scanner and feed updater tests retained in CI.

## Verified CI and asset footprint

- Renderer workflow: `42347170210` — success.
- README validation workflow: `42347242157` — success.
- Five RSS/Atom updater unit tests — passed.
- Public-secret scan — passed.
- README validator — passed: 21 image references resolve, 26 HTML links inspected, one SVG safely parsed, six project artworks, six Technical Focus cards, nine looping GIFs.
- Tracked asset footprint at validated branch head: 2,105,390 bytes of the 3,145,728-byte budget.

## Live rendering and platform limitations

- The actual profile page URL was requested through the available web route, but GitHub returned a cache miss. This environment did not provide a controllable browser session or profile-page screenshots, so actual live GitHub desktop/mobile rendering and dark/light theme inspection cannot be claimed.
- GitHub controls the page background and sanitises README HTML. The README cannot force a page-wide black background, custom CSS, JavaScript, hover behaviour or a guaranteed mobile one-column breakpoint.
- Animated artwork uses self-hosted GIFs; the validator verifies file metadata and CI generation, not GitHub's end-user playback or perceived smoothness.
- The two-column HTML table may remain side-by-side on narrow screens. A GitHub profile browser/device screenshot pass is still required to confirm how the rendered profile behaves at phone widths.
- The original engineering asset is a generated parametric mesh render; no editable CAD source or production-engine model was available.
