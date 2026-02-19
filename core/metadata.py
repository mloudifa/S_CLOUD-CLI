from typing import List
import yt_dlp
from numba.core.types import none

from core.pars import pars_url
import sys

class Song:
    def __init__(self, title: str, url: str, duration: int | None = None):
        self.title = title
        self.url = url
        self.duration = duration

    def __repr__(self):
        return f"Song(Title:{self.title} | Url:{self.url} | Duration:{self.duration})"

# ----------------------------
#   Fetchers
# ----------------------------
def fetch_Scloud_metadata(url: str) -> List[Song]:
    ydl_opts = {"quiet": True, "skip_download": True, "extract_flat": True}
    songs: List[Song] = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"SoundCloud extraction failed: {e}")
            return []
        entries = info.get("entries", [info])
        for e in entries:
            songs.append(Song(title=e.get("title"), url=e.get("url"), duration=e.get("duration")))
    return songs

# ----------------------------#
#   Unified fetch_metadata    #
# ----------------------------#
def fetch_metadata(url: str) -> List[Song]:
    
    parsed = pars_url(url)
    if parsed["type"] in ["INVALID_URL", "INVALID_PLATFORM"]:
        return []
    platform = parsed["platform"]
    if platform == "SoundCloud":
        return fetch_Scloud_metadata(url)
    return []