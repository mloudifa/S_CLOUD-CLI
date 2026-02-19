import csv
import os
import threading

CSV_HEADERS = [
    "Title",
    "Filename",
    "SampleRate_Hz",
    "Duration_s",
    "Estimated_BPM",
    "Bitrate_kbps",
    "Channels",
    "Status"
]

_lock = threading.Lock()

def init_csv(path: str):
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CSV_HEADERS)

def append_row(path: str, row: list):
    with _lock:
        with open(path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)
