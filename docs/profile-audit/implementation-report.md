# Implementation report — 2026-11-07

## Completed changes

- Created recovery branch backup/profile-before-master-rebuild-2026-11-07 from the audited baseline commit.
- Added a baseline repository audit and a visual design-system document.
- Added reference research and adoption decisions with an emphasis on GitHub README constraints and self-hosted media.
- Corrected the Blender GIF verification contract to match the actual 900×225, 10-frame output.
- Increased the 3D render job timeout from 8 to 15 minutes.
- Renamed the decorative city render to engineering-city so it is not misrepresented as contribution analytics.
- Replaced the decorative trophy prop with a precision vernier-caliper model, avoiding an unsupported achievement implication.
- Updated the README to describe verified public project functionality and distinguish decorative artwork from data visualizations.
- Expanded the dashboard generator to paginate public repositories, fail rather than silently omit repository language data, and write an auditable JSON snapshot alongside SVG and PNG.
- Updated the dashboard workflow and README validator to include and validate the JSON data file.
- Removed the duplicate legacy metrics workflow; profile-dashboard.yml is now the only dashboard refresh workflow.
- Updated SETUP.md and added an animation-source guide.

## Current 3D scene inventory

The renderer defines twelve product/engineering scenes: hero turbocharger, piston assembly, processor, laptop, phone, dashboard monitor, precision caliper, industrial campus, keyboard/workbench, notebook, alloy wheel and industrial connector. Each scene is rendered as 10 eased frames at 900×225 and packed to a shared-palette GIF.

The industrial-campus scene is an original decorative architectural scene. It is not a contribution heatmap and is not driven by contribution counts.

## Data and integration decisions

- The dashboard uses public GitHub REST data only.
- Language distribution is measured by repository language byte counts and excludes forks and archived repositories.
- No WakaTime, Spotify, Discord presence or LeetCode widget was enabled because no verified data source/credentials were provided.
- The optional blog feed remains disabled unless BLOG_FEED_URL is configured.
- No new personal token or secret was introduced.

## Pending work

- The current 3D workflow must complete successfully with the final scene names and validation before the new GIFs are promoted into the README.
- A true contribution city requires a reliable source for dated contribution counts. The public REST repository list alone is insufficient; private contributions must not be assumed.
- The final verification report must be updated after the final workflow runs and the resulting GIFs are inspected.
