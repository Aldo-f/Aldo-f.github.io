---
title: "DRM-free at Last: How I Made VRT MAX Watchlist Downloads Work on Raspberry Pi"
date: 2026-09-03
categories:
  - Home Lab
  - Belgium
  - Media
tags:
  - thuis
  - vrt-max
  - drm
  - raspberry-pi
  - podcast-downloader
  - home-lab
  - belgium
  - watchlist
---

VRT MAX streams are DRM-protected and notoriously hard to download. After weeks of work involving pywidevine, N_m3u8DL-RE, and a custom `_vrt_drm_*` field detector, the thuis-v4 downloader now gracefully handles both DRM and non-DRM content. This post covers the full journey — from detecting DRM in the HLS manifest to the fallback strategy that keeps non-DRM downloads fast.

<!-- more -->

## The Problem: Why VRT MAX Refuses to Play Nice

VRT MAX is the streaming platform of Belgium's public broadcaster (VRT). Their content uses Widevine DRM — the same technology Netflix and Spotify use. Standard downloaders like yt-dlp hit a wall: they see the HLS manifest, attempt to download segments, and get encrypted garbage.

The key insight came from inspecting the GraphQL responses: VRT MAX embeds `_vrt_drm_*` fields that explicitly tell you whether content is protected. No guessing, no failed downloads — just read the field and route accordingly.

## The Detection Layer: Classifying Content Before Download

The thuis-v4 downloader uses a two-stage probe in `probe.py` and `drm_decrypt.py`:

1. **GraphQL fetch** — retrieve the episode's streaming metadata including `_vrt_drm_key_id`, `_vrt_drm_license_url`, and `_vrt_drm_protection_scheme`
2. **HLS manifest inspection** — if DRM fields exist, parse the manifest for `#EXT-X-KEY` tags to confirm encryption method (AES-128 vs SAMPLE-AES)

```python
# Simplified detection logic
def classify_content(episode_data: dict) -> ContentType:
    if episode_data.get("_vrt_drm_key_id"):
        return ContentType.DRM_PROTECTED
    # Fallback: inspect HLS manifest for EXT-X-KEY
    manifest = fetch_hls_manifest(episode_data["hls_url"])
    if "#EXT-X-KEY:METHOD=SAMPLE-AES" in manifest:
        return ContentType.DRM_PROTECTED
    return ContentType.CLEAR
```

This runs in milliseconds and prevents wasting bandwidth on content that needs the heavy pipeline.

## The DRM Pipeline: pywidevine + N_m3u8DL-RE

For DRM-protected content, the pipeline is:

1. **License acquisition** — use the `_vrt_drm_license_url` with a Widevine CDM (via pywidevine) to request a license
2. **Key extraction** — parse the license response for the content decryption key
3. **Download with decryption** — feed the key to N_m3u8DL-RE, which handles segment decryption on the fly

```bash
# What the downloader runs under the hood
N_m3u8DL-RE "https://vrt.be/manifest.m3u8" \
  --key "1234567890abcdef:fedcba0987654321" \
  --save-dir "/downloads" \
  --ffmpeg-binary-path "/usr/bin/ffmpeg"
```

The Raspberry Pi 5's 4 ARM Cortex-A76 cores handle this comfortably — a 45-minute episode takes ~3 minutes end-to-end.

## Graceful Fallback: The `_nodrm_` Path

Here's the part I'm proud of: **non-DRM content skips the entire decryption stack**. No CDM initialization, no license request, no N_m3u8DL-RE overhead. Just a direct `ffmpeg -i <hls_url> -c copy <output>` — completes in seconds.

The watchlist feature (see below) automatically routes each episode to the right path based on the detection result. You configure shows, not pipelines.

## Watchlist Magic: Set It and Forget It

The real UX win is the watchlist system. Create a text file:

```text
# watchlists/tv.txt
[daily]
Het Journaal
Terzake

[weekly]
De Slimste Mens
Villa Politica
```

Run `./thuis.sh --watchlist watchlists/tv.txt` via cron (or systemd timer) and it:
- Checks for new episodes of each show
- Classifies each episode (DRM vs clear)
- Downloads using the appropriate pipeline
- Respects `--dry-run` for testing

The `[daily]` / `[weekly]` directives control scheduling granularity — no external scheduler needed.

## What I Learned: The Reality of CDM Licensing

Three hard-won lessons:

1. **CDM licensing is fragile** — Widevine CDMs have device limits and expiration. The downloader caches licenses and retries automatically, but some episodes simply won't play if the CDM is revoked.

2. **Not all episodes are equal** — Even within a series, some episodes are DRM-protected and others aren't (e.g., news vs drama). The per-episode detection handles this automatically.

3. **Testing discipline pays off** — 3,800+ lines of tests cover the detection logic, mock GraphQL responses, HLS manifest parsing, and end-to-end download flows. Every bug found in production became a regression test.

## The Result

What started as "can I download *De Slimste Mens* for offline viewing?" became a robust, self-hosted pipeline that:
- Runs on a €80 Raspberry Pi 5
- Handles both DRM and non-DRM content transparently
- Schedules via simple watchlist files
- Produces standard MP4/MKV files playable anywhere

The code lives in `~/dev/06-apps-thuis-v4` (submodule in the home-lab monorepo). The watchlist feature is documented in `watchlists/README.md`.

---

*This post is based on commits `dc1f9d6` (DRM detection), `24403d2` (pywidevine integration), `bb4036e` (watchlist scheduler), and `7bafb52` (fallback optimization) in the thuis-v4 repository. All commits and test runs are verifiable in the `~/dev` git history.*