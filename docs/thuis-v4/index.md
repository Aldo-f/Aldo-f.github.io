# Thuis

VRT MAX downloader using yt-dlp with Widevine DRM support.

![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **yt-dlp based** - Uses patched yt-dlp for VRT MAX authentication and streaming
- **DRM Support** - Decrypt Widevine DRM content with N_m3u8DL-RE or mp4decrypt
- **Watchlist Mode** - Process multiple URLs from text files with scheduling (`[daily]`, `[weekly]`)
- **Transcoding** - Convert downloads to 720p with FFmpeg
- **Resume Handling** - Automatically handles interrupted downloads
- **Season/Show Download** - Download entire seasons or all episodes of a show
- **Normalize** - Rename video files to consistent scene format

---

## Quick Start

```bash
# Clone the repository
git clone <repository-url> thuis
cd thuis

# Create a virtual environment
uv venv --link-mode=hardlink
uv pip install -r requirements.txt

# Download a video
./thuis.sh https://www.vrt.be/vrtmax/a-z/thuis/
```

---

## Requirements

| Requirement | Description |
|-------------|-------------|
| Python 3.8+ | Required for type hints |
| ffmpeg | Required for transcoding |
| yt-dlp | Installed via requirements.txt |
| VRT MAX account | Required for authentication |

---

## Links

- [Installation](installation.md)
- [Usage](usage.md)
- [DRM Setup](drm.md)
- [Requirements](REQUIREMENTS.md)
- [GitHub](https://github.com/Aldo-f/thuis)
