# Cyberpunk engineering portfolio — visual system

## Protected identity

The approved README opening block and `assets/hero/engineering-hero.svg` are not part of the redesign. Their exact source is locked in `scripts/validate_profile_readme.py`. The Hero SVG blob must remain `f988a3193de32412396a760fee2cf46d7de771e4`.

## Direction

Premium engineering editorial with a restrained cyberpunk treatment: deep-black artwork fields, fine technical grids, crisp typography, carefully used electric accents and real project context. The design is not a gaming HUD and avoids decorative data, fake activity and unsupported claims.

## Palette

| Token | Hex | Usage |
|---|---|---|
| Black | `#050608` | Artwork backgrounds |
| Secondary surface | `#0B0F16` | Interface panels |
| Elevated surface | `#111722` | Product UI cards |
| Primary text | `#F2F5FA` | High-contrast labels |
| Secondary text | `#A5B0C0` | Supporting copy |
| Electric cyan | `#00E5FF` | Primary accent / system signal |
| Neon violet | `#9D5CFF` | Secondary accent |
| Magenta | `#FF3CAC` | Selective warning / system highlight |
| Acid lime | `#C7FF4A` | Approval / positive status only |
| Border | `#253344` | Quiet surface separation |

Cyan is the dominant accent. Violet and magenta distinguish selected projects. Lime is used sparingly for an explicit approval/status signal.

## Typography and layout

- Essential copy remains real README text, not rasterised text.
- Use native GitHub headings, paragraphs, links and tables; no external fonts or custom CSS.
- Project art uses consistent 1200×520 JPEG frames, but each composition is different and based on the actual project UI or workflow.
- Technical focus and education are separate editorial visuals, followed by accessible text.
- The GitHub page background is controlled by the user's selected GitHub theme. The README cannot force a page-wide black background; the artwork itself uses the specified black surfaces and remains readable in both themes.

## Project visuals

1. VisaFlowX — extension dashboard study with monitor rules and an explicit manual protected-verification gate.
2. Kostenlos AI — chat workspace study with BYOK and the documented Groq, Gemini, OpenAI and Mistral route.
3. Noti-Fixer — phone pairing and ADB diagnostic scene with a read-only review and user-approval boundary.
4. Circle to Search — HyperOS gesture and native Google invocation route; device eligibility remains visible.
5. Smart Scanner Pro — scanner/architecture concept, with planned features explicitly labelled.

These are original visual studies generated from public repository READMEs and source. They are not represented as real application screenshots.

## Engineering 3D

`assets/engineering/piston-connecting-rod-crankshaft.jpg` is rendered from original parametric triangle meshes: piston skirt and crown, ring geometry, wrist pin, connecting rod, big-end bearing, crank webs, crank pin and main journal. A small painter's renderer applies camera projection, face lighting, metallic highlights and depth sorting. Source is in `tools/render_portfolio_art.py`; it uses Pillow only. It is an engineering study, not a depiction of a named production engine.

## Motion

- One self-hosted signal-sweep GIF: 560×84, 24 frames, 220 ms/frame, 5.28-second loop.
- The movement is a single low-density cyan scan line; all labels remain static.
- GIF is visual only and has no interaction. Its first frame is a usable still if motion is paused.
- Project cards and data charts remain static so the text and values stay legible.
- No new SVG SMIL animation is relied upon.

## Data integrity

`assets/data/public-repositories.json` is the source for the accompanying chart. Snapshot date: 2026-11-07. Scope: seven public project repositories; the profile repository and private repositories are excluded. Counts: 13 stars, 4 forks. Primary language counts: JavaScript 2, TypeScript 2, C# 1, PowerShell 1, Python 1. The language metric counts repositories, not source bytes or personal skill. Contribution data is not duplicated; GitHub's native graph remains authoritative.

## Accessibility and compatibility

- Descriptive alt text is provided for meaningful images.
- Important facts remain in README text.
- No rapid flashing, strobing or animated text.
- No custom CSS, JavaScript, hover event, external image host or web font.
- JPEGs are static; GIF is a visual loop. The profile README does not provide a reliable reduced-motion preference hook.
- GitHub sanitisation and client behaviour can vary. Source validation does not prove that GitHub displays every image or animation identically on desktop, mobile, dark and light themes.

## Asset budgets and CI

- Total `assets/` budget: 800 KiB.
- Individual generated raster/GIF asset budget: 150 KiB.
- Project JPEGs: 1200×520.
- Technical focus: 1200×360.
- Education path: 1200×300.
- Public analytics: 1200×360.
- GIF: 560×84, 24 frames, 220 ms/frame.
- CI locks the Hero, resolves local README references, parses SVG, validates raster dimensions and GIF frame metadata, scans common secret patterns and runs the optional feed updater tests.
