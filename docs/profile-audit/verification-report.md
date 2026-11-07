# Verification report — 2026-11-07

## Verified

- Baseline recursive repository tree and README were retrieved from GitHub.
- Existing assets were preserved; no existing artwork or approved snake file was deleted.
- Backup branch backup/profile-before-master-rebuild-2026-11-07 was created from the recorded baseline commit.
- The previously approved snake GIF remains at assets/section-08-contribution-snake.gif and its historical blob identity was verified in the prior audit.
- GitHub Actions run 42338451088 completed successfully: all 12 Blender scenes rendered, all 12 GIFs were packed and validated at 900×225 with 10 frames each, and the README was switched to the new self-hosted media. The render job took approximately 6 minutes from job start through commit.
- The same run generated a real GitHub GraphQL contribution calendar: 348 contributions across 366 returned days and 53 weeks; daily counts sum exactly to 348. Private contribution visibility was false and restricted count was 0.
- Both render workflows now use a 15-minute timeout and the corrected 900×225, 10-frame validation contract.
- The dashboard workflow successfully completed at least one run after the JSON data output was introduced: https://github.com/shovo127/shovo127/actions/runs/42336145509
- The repository now includes assets/github-dashboard-data.json.
- Duplicate metrics.yml was removed.
- Project descriptions were checked against public repository README content for Kostenlos AI, VisaFlowX, VisaFlowX Universal, Noti-Fixer, Circle to Search for Xiaomi and IPTV By Shovo.

## Not yet verified

- A second render is in progress to add visible camera dolly/orbit and warm rim-light movement; its output must pass the same full verification before it is considered final.
- Human visual inspection of every rendered GIF is not available through the current GitHub file connector; technical GIF checks are automated and successful.
- The final README alt-text/static-SVG-link commit was checked manually for all local image paths (18/18 resolve, zero remote image hosts).
- Optional WakaTime, Spotify, Discord, RSS and LeetCode integrations; they remain disabled unless configured with authentic data and credentials.

## Known limitations

- The current snake workflow verifies the preserved GIF; it does not regenerate it.
- The contribution city is data-driven. It uses GitHub GraphQL daily counts; private contributions are not visible in this account snapshot (restricted count 0).
- The dashboard uses public GitHub API data. API failures should stop generation rather than publish partial language totals.
- A successful GitHub Actions run validates technical properties but does not replace human visual judgement of composition and motion.

## Status

The first complete 12-scene render and automated README QA passed. A follow-up render adding camera and lighting movement is still in progress; do not mark the motion upgrade complete until that run and its downstream README checks pass.
