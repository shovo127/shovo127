# Animation source files

The repository-owned Blender source is currently maintained in:

- scripts/render_profile_3d.py — scene geometry, materials, lighting, camera and keyframes.
- scripts/pack_profile_3d.py — shared-palette GIF packaging and output checks.

The profile-assets.yml workflow downloads the official checksum-verified Blender release, renders temporary PNG frames on the runner, packs the GIFs and commits only validated final outputs to assets/3d/.

## Render settings

- Blender: 4.5.15, Eevee Next, software rendering on Ubuntu GitHub-hosted runners.
- Output canvas: 900 × 225 pixels.
- Animation: 10 frames per scene, 120 ms per frame, infinite loop.
- Sampling: 6 Eevee temporal anti-aliasing render samples.
- Colour management: AgX when available, Filmic fallback.
- Materials: Principled BSDF with metallic/roughness values and fine noise bump.
- Lighting: large cool key, cool edge strip, warm rim and front fill.
- Motion: eased turntable rotation from −18° to +18° and back, a small vertical bob, a camera dolly/orbit offset, and a warm rim-light intensity sweep. First and last keyframes match for a seamless loop.
- GIF packaging: shared 96-colour palette across each scene's frames, Floyd–Steinberg dithering, Pillow.
- Contribution city: 52/53-week isometric calendar grid driven by assets/contribution-city-source.json, the immutable snapshot committed with the 3D render. Missing data yields a neutral flat grid.


The source files are intentionally kept as readable Python scripts instead of opaque .blend binaries. This makes the scene definitions reviewable in Git diffs and reproducible in GitHub Actions.

- scripts/fetch_contribution_data.py — retrieves the official GitHub GraphQL contribution calendar using the built-in GITHUB_TOKEN for public counts and optional PROFILE_READ_TOKEN for private counts, writes a dated JSON snapshot and static isometric SVG, and emits an explicit neutral empty state when data is unavailable. The workflow copies this live JSON to assets/contribution-city-source.json before rendering; the Blender contribution-city scene reads that committed snapshot so its building heights and colours reflect the exact source counts.
- scripts/generate_contribution_snake.py — simulates a collision-free continuous route through the dated calendar. Food markers exist only on days with non-zero contribution counts; the snake grows when it reaches those days. The resulting GIF is a non-interactive visualization, not a playable game. The previously approved classic snake GIF remains separately preserved.

scripts/audit_profile_assets.py records dimensions, animation frames, timing, sizes and SHA-256 for every asset under assets/. Its deterministic inventory is checked in CI.

The previously approved classic contribution snake remains byte-for-byte preserved at assets/section-08-contribution-snake.gif. The new data-driven snake is generated separately by scripts/generate_contribution_snake.py.
