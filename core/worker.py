import os
import time
import uuid
import librosa
import soundfile as sf
from yt_dlp import YoutubeDL

class SilentLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def process_song(song, output_dir, max_retries=3, sleep_between_retries=1):
    """
    Downloads song/playlist, converts to WAV, analyzes BPM.
    Uses unique temp filenames to prevent Windows file locks.
    Returns list of result dicts.
    """
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(output_dir, "tmp")
    os.makedirs(temp_dir, exist_ok=True)

    # Unique identifier for this download (avoids .part collisions)
    unique_id = str(uuid.uuid4())[:8]

    # Safe output template
    outtmpl = os.path.join(temp_dir, f"{unique_id}-%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "merge_output_format": "mp4",       # merge fragments safely
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
        "postprocessor_args": ["-ar", "48000"],
        "quiet": True,
        "logger": SilentLogger(),
        "noplaylist": True,
        "js_runtime": "deno",
        "http_headers": {"User-Agent": "Mozilla/5.0"},
        "extractor_args": {
            "soundcloud": {},
            "youtube": {"player_client": ["web"], "allow_unplayable_formats": True},
            "youtube:music": {"player_client": ["web"]}
        }
    }

    attempt = 0
    results = []

    while attempt < max_retries:
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song.url, download=True)

            entries = info.get("entries", [info])
            for entry in entries:
                # WAV path in temp folder
                wav_temp_path = ydl.prepare_filename(entry).rsplit(".", 1)[0] + ".wav"

                # Safe final path in output_dir
                safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in entry.get("title", song.title))
                wav_final_path = os.path.join(output_dir, f"{safe_title}.wav")

                # Atomic move (rename temp -> final)
                if os.path.exists(wav_temp_path):
                    try:
                        os.replace(wav_temp_path, wav_final_path)
                    except Exception as e:
                        return [{"title": song.title, "error": f"Failed to move file: {e}", "status": "failed"}]

                results.append(_analyze_wav_safe(wav_final_path, entry.get("title", song.title)))

            return results

        except Exception as e:
            attempt += 1
            time.sleep(sleep_between_retries)
            if attempt >= max_retries:
                return [{"title": song.title, "error": str(e), "status": "failed"}]

    return [{"title": song.title, "error": "Unknown error", "status": "failed"}]


def _analyze_wav_safe(wav_path, title):
    """Analyze WAV file safely"""
    try:
        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            return {"title": title, "error": "Downloaded file is empty", "status": "failed"}

        y, sr = librosa.load(wav_path, sr=None, mono=False)
        duration = float(librosa.get_duration(y=y, sr=sr))

        try:
            y_mono = librosa.to_mono(y)
            tempo, _ = librosa.beat.beat_track(y=y_mono, sr=sr)
            status = "ok"
        except Exception:
            tempo = 0.0
            status = "partial"

        info_sf = sf.info(wav_path)
        bitrate = sr * info_sf.channels * 24 / 1000

        return {
            "title": title,
            "filename": os.path.basename(wav_path),
            "samplerate": sr,
            "duration": duration,
            "bpm": float(tempo),
            "bitrate": bitrate,
            "channels": info_sf.channels,
            "status": status
        }

    except Exception as e:
        return {"title": title, "error": str(e), "status": "failed"}
