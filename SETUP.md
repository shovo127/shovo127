# Profile integrations setup

The core profile is designed to work without external credentials.

## GitHub Metrics
The Metrics workflow initially uses the repository's built-in `GITHUB_TOKEN`. For extended read access, create a fine-grained token limited to the required repository/user read scopes, then add it as `METRICS_TOKEN`. Never commit tokens.

## WakaTime
1. Create a WakaTime account and install its editor plugin.
2. Add repository secret `WAKATIME_API_KEY` in Settings → Secrets and variables → Actions.
3. Use a maintained WakaTime integration and follow its current documented input names. Do not publish a fabricated coding-hours report.

## Blog / RSS
Add a repository variable called `BLOG_FEED_URL` under Settings → Secrets and variables → Actions → Variables. Set it to a public RSS or Atom feed. The workflow inserts up to five posts.

## Spotify
A Spotify README integration requires Spotify OAuth authorization and usually a client ID, client secret, refresh token, and username. Add secrets only after choosing and reviewing the integration. Never commit credentials.

## LeetCode
Add your LeetCode username when ready. Use a maintained stats provider or a scheduled workflow that obtains your public profile data. Verify the provider before relying on its ranking data.

## Discord
Discord Rich Presence is local desktop activity and is not exposed to a static README. A third-party service needs explicit authorization and secure hosting. Never publish Discord bot tokens.

## Skill radar / wheel
A skill wheel should use self-assessed levels or verified repository data. Source-code percentages are not the same as proficiency. Add data only after defining and checking the method.

## Photo / video
The profile currently uses your GitHub avatar. Add a portrait or animated GIF only when you upload an image you have permission to publish. GitHub README pages do not support video as a background.
