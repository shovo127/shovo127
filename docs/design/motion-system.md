# Motion and visual system

**Scope:** GitHub profile README and repository-owned media.  
**Direction:** restrained engineering editorial; precise, calm and readable.

## Protected identity layer

- The approved Hero is the first README block: hero image, name, positioning line and contact line, ending at the first horizontal divider.
- The Hero SVG is protected by a Git blob SHA check in CI. The README's approved opening block is also compared byte-for-byte.
- Phase 2 work must not alter, reposition, restyle or rewrite this block.

## Visual language

| Token | Rule |
|---|---|
| Base | Deep slate / graphite with restrained desaturated green-metal accents |
| Contrast | Light neutral text against dark illustration fields; all key copy remains normal README text |
| Geometry | Fine rules, aligned technical grids and schematic connectors |
| Typography | Native GitHub Markdown headings and restrained system typography inside SVGs |
| Density | One clear idea per project visual; avoid decorative badges and redundant metrics |
| Spacing | Native Markdown paragraph spacing and consistent section separators |

## Project visual system

- Five self-hosted project illustrations use a shared 1120 px canvas, 300 px or 260 px height, rounded graphite field, thin technical grid and muted metal palette.
- The illustrations are original schematic diagrams, not product screenshots or claims that a UI exists.
- Each image has an explicit title, description and README alt text.
- Project descriptions and stacks are sourced from each public repository's README or architecture documentation.
- Smart Scanner Pro is explicitly described as architecture-first; its README labels its advertised feature set as planned.

## Motion policy

| Element | Treatment | Status |
|---|---|---|
| Approved hero rotor | Existing 24 s SVG rotation | Preserved; playback on GitHub clients not independently verified |
| Section rule | Existing low-frequency SVG line animation | Preserved; static line remains if SMIL is not played |
| Project visuals | Static diagrams | Deliberate: no movement needed to understand the architecture |
| Contribution data | GitHub native UI | No duplicate third-party widget or unverified animation |

Motion is not used to carry information. GitHub README SVG is rendered in an image context; arbitrary CSS, JavaScript, hover behaviour and a reliable reduced-motion signal are unavailable. SVG SMIL may be sanitized, paused or rendered differently across clients. Therefore the static artwork remains complete and readable.

## Responsiveness and compatibility

- Project cards use a two-column HTML table with image widths set to 100%; GitHub clients may stack, shrink or horizontally scroll tables differently at narrow widths.
- No custom CSS or JavaScript is embedded.
- No external image hosts, web fonts, scripts or runtime statistics services are required.
- The README uses relative, case-sensitive repository paths.
- Actual GitHub mobile, desktop, dark-theme and light-theme screenshot checks remain a manual browser QA step.

## Asset budget

- Hero SVG: 3,984 bytes (existing, protected).
- Project SVGs: self-hosted, vector and text-light.
- Total repository assets budget enforced by CI: 200 KiB.
- Individual SVG budget enforced by CI: 64 KiB.
- No GIF or video is added without a human-reviewed rendered output and GitHub Markdown compatibility test.

## Accessibility

- Essential information stays in Markdown text.
- Meaningful images have descriptive alt text; decorative dividers use empty alt text.
- No flashing, strobing, bouncing or animated text.
- Static frames remain understandable if animation is disabled.
- Colour is not the only carrier of meaning.

## Quality gates

- CI locks the approved Hero README block and Hero SVG blob.
- CI parses every SVG as XML and rejects script/foreignObject and remote SVG references.
- CI checks README-local image/link paths, case-sensitive existence and total asset size.
- Browser rendering, animation playback and native profile layout require visual inspection on GitHub itself.
