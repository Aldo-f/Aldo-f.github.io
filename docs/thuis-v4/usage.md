---
sidebar_position: 3
---

# Usage

You can run thuis in two ways: using the wrapper script or by calling the Python module directly.

## Wrapper script (easiest)

```bash
./thuis.sh https://www.vrt.be/vrtmax/a/show/...
```

## Direct Python

```bash
python -m thuis.main https://www.vrt.be/vrtmax/a/show/...
```

## Examples

### Download a single video

```bash
./thuis.sh https://www.vrt.be/vrtmax/a/show/...
```

### Download multiple videos at once

```bash
./thuis.sh https://www.vrt.be/vrtmax/a/show/1/ https://www.vrt.be/vrtmax/a/show/2/ https://www.vrt.be/vrtmax/a/show/3/
```

### Download videos from a URL file

Create a text file with one URL per line (blank lines and lines starting with `#` are ignored):

```
# my-list.txt
https://www.vrt.be/vrtmax/a/show/1/
https://www.vrt.be/vrtmax/a/show/2/
```

Then run:

```bash
./thuis.sh --file my-list.txt
```

### Dry run (see what would be downloaded)

```bash
./thuis.sh --dry-run https://www.vrt.be/vrtmax/a/show/...
```

### Custom output directory

```bash
./thuis.sh --output-dir ~/Videos https://www.vrt.be/vrtmax/a/show/...
```

### Download a full season

Pass a season URL to download every episode in that season:

```bash
# By season number in path
./thuis.sh https://www.vrt.be/vrtmax/a-z/fc-de-kampioenen/2/

# By query parameter
./thuis.sh 'https://www.vrt.be/vrtmax/a-z/fc-de-kampioenen/?seizoen=seizoen-2'
```

### Download all seasons of a show

Pass a bare show URL (without a season number) to automatically discover and download every season:

```bash
./thuis.sh https://www.vrt.be/vrtmax/a-z/thuis
```

The tool queries the show page, detects all available seasons via the VRT MAX GraphQL API, and expands each into its episodes.

### Limit episodes

Use `--max-episodes` to limit the number of episodes processed per season:

```bash
# Download at most 5 episodes per season
./thuis.sh --max-episodes 5 https://www.vrt.be/vrtmax/a-z/fc-de-kampioenen/2/

# Limit across all seasons (show-level URL)
./thuis.sh --max-episodes 10 https://www.vrt.be/vrtmax/a-z/thuis
```

### Enable console logging

By default, logs are written to `logs/` directory only. Use `--log-level` to see them in the console:

```bash
./thuis.sh --log-level DEBUG https://www.vrt.be/vrtmax/a/show/...
```

### Follow log output

To tail the latest log file in real-time:

```bash
./thuis.sh --follow
```

### Limit video resolution

Use `--profile` (or `-p`) to cap the output resolution. Valid values are 720, 1080, 1440, and 2160:

```bash
./thuis.sh --profile 720 https://www.vrt.be/vrtmax/a/show/...
```

This restricts the best video format to the given height. For example, `--profile 720` downloads 720p max even if higher resolutions are available.

### Retry mode

Use `--retry` to skip downloads where the output file already exists:

```bash
./thuis.sh --retry https://www.vrt.be/vrtmax/a/show/...
```

When set, the tool checks if the destination file is already on disk and skips the download instead of overwriting. This is useful for re-running on a partially completed list without re-downloading existing files.

### Watchlist Mode

Process multiple URLs from text files with optional scheduling. Each series has its own watchlist file.

```bash
# Dry run a single watchlist
./thuis.sh --watchlist watchlists/Fc_De_Kampioenen.txt --dry-run

# Process manual entries (requires --now)
./thuis.sh --watchlist watchlists/Fc_De_Kampioenen.txt --now

# Process multiple series at once
./thuis.sh --watchlist watchlists/Fc_De_Kampioenen.txt \
           --watchlist watchlists/Flikken.txt \
           --watchlist watchlists/Flikken_Maastricht.txt \
           --watchlist watchlists/Thuis.txt \
           --now --dry-run

# Process podcasts (scheduled entries run automatically, manual need --now)
./thuis.sh --watchlist watchlists/podcast.txt --now --dry-run
```

#### Watchlist File Format

1. **First non-comment line**: Output directory (absolute, relative, or `~/` expanded)
2. **Subsequent lines**: URL entries with optional schedule

| Schedule | Meaning |
|----------|---------|
| (none) | Manual entry — requires `--now` flag |
| `[daily]` | Run once per day |
| `[weekly]` | Run once per week |
| `[weekdays 10:00]` | Run weekdays at given time |

```text
# watchlists/podcast.txt
/mnt/HDD1/nextcloud/data/aldo/files/Media/podcasts/_seed

# De Gifmenger (manual — needs --now)
/mnt/HDD1/nextcloud/data/aldo/files/Media/podcasts/_seed
https://www.vrt.be/vrtmax/podcasts/ketnet/w/waanzinnig-maar-waar--/

# Scheduled entries run automatically from cron
[weekly] https://www.vrt.be/vrtmax/podcasts/ketnet/w/waanzinnig-maar-waar--/
```

#### Example Watchlist Files

| File | Output | Schedule |
|------|--------|----------|
| `watchlists/Fc_De_Kampioenen.txt` | TV (`tv/`) | Manual |
| `watchlists/Flikken.txt` | TV (`tv/`) | Manual |
| `watchlists/Flikken_Maastricht.txt` | TV (`tv/`) | Manual |
| `watchlists/Thuis.txt` | TV (`tv/`) | Manual |
| `watchlists/podcast.txt` | Podcasts (`_seed/`) | Weekly |

## Example output

```
$ ./thuis.sh --dry-run https://www.vrt.be/vrtmax/a/show/some-episode
[thuis] Found 1 video(s)
[1/1] Processing: https://www.vrt.be/vrtmax/a/show/some-episode
Running: /path/to/.venv/bin/python3 -m yt_dlp -f bestaudio --no-warnings \
  --username kuxelu@ipdeer.com --password *** \
  -o /path/to/output/Some.Episode.m4a \
  https://ondemand-radio.vrtcdn.be/...
Downloading: Some Episode (2025-04-07).m4a
Done: Some Episode (2025-04-07).m4a
```

Secrets (`--password`) are masked as `***` in the console `Running:` line.

## Normalize video files

Rename video files in a directory to a consistent scene format:

```bash
thuis normalize /path/to/videos
```

Options:

| Flag | Description |
|------|-------------|
| `--dry-run` | Show what would happen without making changes |
| `--cleanup` | Remove duplicates (`_1` suffix) and stale `.part` files |

```bash
# Preview changes
thuis normalize --dry-run /path/to/videos

# Normalize and clean up
thuis normalize --cleanup /path/to/videos
```

## Log output

By default, logs are written to `logs/` only. Use `--log-level` to see them in the console:

```bash
./thuis.sh --log-level DEBUG https://www.vrt.be/vrtmax/a/show/...
```

To tail the latest log file in real-time:

```bash
./thuis.sh --follow
```

