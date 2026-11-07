# Graphite, teal and champagne engineering profile

## Design direction

A premium engineering editorial system built around graphite, deep teal, champagne and ice. The earlier red/black treatment is retired. Artwork uses a quiet technical grid, metallic neutrals, controlled accent contrast and high-legibility typography. GitHub controls the surrounding profile-page surface and theme; the README cannot impose a page-wide background or responsive CSS.

## Palette

| Token | Hex | Usage |
|---|---|---|
| Graphite background | `#09111B` | Main artwork field |
| Slate surface | `#111E2B` | Card and title surfaces |
| Deep teal | `#243B4B` | Structural lines |
| Primary teal | `#3EC6B5` | Active systems and motion |
| Champagne | `#DAB171` | Secondary highlights |
| Ice | `#BADCDF` | Fine detail and secondary emphasis |
| Main text | `#EBF3F6` | Titles and key labels |
| Secondary text | `#9BB1BC` | Descriptions |
| Border | `#243A48` | Card boundaries |

## Motion grammar

Every visual family has a distinct movement chosen to match its subject:

| Area | Motion treatment |
|---|---|
| Hero | Continuously rotating precision rotor |
| Hero name and tagline | Letter-by-letter typewriter reveal with a blinking cursor |
| Section headings | Individual typewriter title loops |
| VisaFlowX | A route marker travels through workflow nodes |
| Kostenlos AI | A response is typed into a chat bubble |
| Noti-Fixer | Notification pulse and device vibration |
| Circle to Search | Expanding target reticle |
| Smart Scanner | Vertical document-feed scan with registration corners |
| IPTV | Independent playlist equaliser bars |
| Software Engineering | Terminal command typing |
| AI & Automation | Neural nodes activate in sequence |
| Android Systems | Concentric notification ripple |
| Automotive Engineering | Reciprocating piston motion |
| Learning Technology | Page-turn and learning-progress reveal |
| Mechanical Visualisation | Orbital wireframe rotation |
| Education | Sequential timeline progress and milestone activation |
| Analytics | Dated snapshot bars animate to their fixed totals; data itself remains static |
| Dividers | Separate waveform, orbital-node, network, chart and mechanical-ring loops |

Project and Technical Focus motion files are individually generated; they do not share a generic left-to-right scan. Title GIFs retain the actual title in their image and descriptive alt text. Supporting descriptions, facts, links and accessibility copy remain normal README text.

## GitHub rendering constraints

The profile is a GitHub README, not a hosted web application. GitHub's documentation states that SVGs do not support inline scripting or animation in GitHub rendering. Therefore, dependable motion is delivered through self-hosted GIFs. The README does not attempt to run JavaScript, custom CSS, hover handlers, iframes or animation libraries. Source: https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files

GitHub controls the page background, theme, image proxy and mobile table layout. The two-column project/focus tables cannot be guaranteed to collapse into a single column on every device. Live browser screenshots are required to certify actual desktop/mobile rendering; CI can validate files and markup but cannot certify the user's browser playback.

## Performance

- Only assets referenced by the README are part of the profile's image payload; retained historical assets are not loaded unless referenced.
- Current README GIF references are approximately 4.6 MB in aggregate.
- Individual GIF limit: 750 KiB.
- Total tracked asset limit: 12 MiB.
- GIF frame count, infinite loop metadata, frame timing, dimensions, local links, SVG safety and image availability are checked by CI.
- New versioned image paths are used when replacing animated artwork to avoid stale image-proxy cache entries.

These are measured repository constraints, not a claim that every browser/device will decode or play every GIF at identical speed.

## Ownership and copying

A public profile README and its public assets can be cloned, downloaded, screenshotted or re-created. GitHub cannot technically prevent that while the repository remains public. Copyright notices and an explicit licence choice can clarify ownership and permitted reuse, but cannot stop copying itself. No anti-copy JavaScript or browser restriction is used.

## Data integrity

The repository analytics remain a dated GitHub REST API snapshot. Its figures are not live counters and are not altered by the animation. Project descriptions continue to distinguish implemented behaviour from planned scope and retain their documented safety boundaries.
