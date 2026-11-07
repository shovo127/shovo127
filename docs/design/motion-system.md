# Motion system

**Scope:** GitHub profile README and repository-owned SVG media.  
**Direction:** restrained engineering editorial; precise, calm and readable.

## Principles

1. Motion has one job: establish hierarchy or reinforce the engineering theme.
2. Keep the name, role and project descriptions static. Essential information never depends on animation.
3. Prefer one slow mechanical movement and short line reveals over decorative loops.
4. Keep contrast and text legibility stable throughout every frame.
5. A static SVG frame must remain a complete composition when animation is unsupported.

## Timing and easing

| Motion | Duration | Easing | Repeat |
|---|---:|---|---|
| Hero entrance | 700 ms | cubic-bezier(0.22, 1, 0.36, 1) | once |
| Technical line reveal | 1,400 ms | ease-in-out | once / low-frequency |
| Mechanical rotor | 24 s | linear | seamless |
| Ambient highlight | 8 s | ease-in-out | alternate |
| Section rule | 2.4 s | ease-in-out | low-frequency |

## Hierarchy and density

- Level 1: one hero composition at the top of the README.
- Level 2: one thin section rule between major content groups.
- Level 3: no animated project cards, text, counters or status indicators.
- Maximum visible looping elements in the README: two.
- No typing loops, flashing, bouncing, particle fields or continuous text movement.

## GitHub compatibility

GitHub profile READMEs are Markdown documents, not web applications. They do not provide arbitrary CSS, JavaScript, hover handlers or a guaranteed animation runtime for SVG. SVG is used because it scales cleanly and includes a useful static composition. The SVG contains native SMIL animation only; if GitHub sanitizes or pauses it, the still frame remains the intended fallback. Motion is not claimed to be verified on every GitHub client.

No external image hosts, fonts, scripts or runtime services are required.

## Accessibility

- Provide descriptive alt text for meaningful images.
- Use empty alt text for decorative section rules.
- Keep all essential profile content as normal Markdown text.
- Avoid rapid luminance changes, flashing and strobing.
- Honour reduced-motion preferences in any future standalone web implementation. GitHub README SVG cannot reliably read the viewer OS preference, so the static frame must remain understandable.
- Maintain a minimum 4.5:1 contrast target for normal text in future interactive web versions.

## Asset budget

- Hero SVG: target ≤ 20 KB.
- Section rule SVG: target ≤ 4 KB.
- No GIF or video in the README until a human-reviewed animation has been rendered, optimized and verified in GitHub Markdown.
- Keep total README visual assets below 25 KB where practical.

## Review checklist

- [ ] Static frame communicates the full message.
- [ ] No text is clipped at narrow widths.
- [ ] Animation is subtle and does not affect readability.
- [ ] SVG parses as XML.
- [ ] README uses repository-relative image paths.
- [ ] No remote image dependency or unverified statistic is introduced.
- [ ] Actual GitHub rendering is checked after publication.
