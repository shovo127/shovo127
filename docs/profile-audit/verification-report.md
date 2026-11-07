# Verification report — 2026-11-07

## Verified

- Baseline recursive repository tree and README were retrieved from GitHub.
- Existing assets were preserved; no existing artwork or approved snake file was deleted.
- Backup branch backup/profile-before-master-rebuild-2026-11-07 was created from the recorded baseline commit.
- The previously approved snake GIF remains at assets/section-08-contribution-snake.gif and its historical blob identity was verified in the prior audit.
- GitHub Actions logs for run 42276737575 confirm all twelve Blender scenes rendered and twelve GIFs were packed. That run failed only because its validator expected 12 frames at 960×240 while the packer emitted 10 frames at 900×225.
- Both render workflows now use a 15-minute timeout and the corrected 900×225, 10-frame validation contract.
- The dashboard workflow successfully completed at least one run after the JSON data output was introduced: https://github.com/shovo127/shovo127/actions/runs/42336145509
- The repository now includes assets/github-dashboard-data.json.
- Duplicate metrics.yml was removed.
- Project descriptions were checked against public repository README content for Kostenlos AI, VisaFlowX, VisaFlowX Universal, Noti-Fixer, Circle to Search for Xiaomi and IPTV By Shovo.

## Not yet verified

- Final 3D media generation and publication after the precision-caliper and engineering-city scene changes.
- Final visual review of every newly rendered GIF from the committed repository.
- The README check workflow after the JSON schema validation change.
- Final 3D render and publication of the new contribution city, including its neutral fallback if PROFILE_READ_TOKEN is not configured.
- Contribution data retrieval with PROFILE_READ_TOKEN; private contribution counts depend on read:user scope and the account's profile setting.
- Optional WakaTime, Spotify, Discord, RSS and LeetCode integrations; they remain disabled unless configured with authentic data and credentials.

## Known limitations

- The current snake workflow verifies the preserved GIF; it does not regenerate it.
- The current engineering-city artwork is decorative and is not mapped to contribution intensity.
- The dashboard uses public GitHub API data. API failures should stop generation rather than publish partial language totals.
- A successful GitHub Actions run validates technical properties but does not replace human visual judgement of composition and motion.

## Status

The repository is improved but the complete acceptance criteria are not yet met. Do not describe the rebuild as finished until the final render workflow, README checks, local asset-reference checks and final repository state have all been verified.
