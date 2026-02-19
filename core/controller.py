from concurrent.futures import ThreadPoolExecutor, as_completed
from core.csv_worker import append_row
from core.worker import process_song

def run_pipeline(songs, output_dir, csv_path, max_workers=4):

    total = len(songs)
    print(f"🎵 Processing {total} track(s)\n")

    results = []

    max_workers = min(max_workers, total)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_song, song, output_dir): idx+1 for idx, song in enumerate(songs)}

        for future in as_completed(futures):
            index = futures[future]
            try:
                song_results = future.result()
                print(f"[{index}/{total}] {song_results}")
            except Exception as e:
                song_results = [{"title": "Unknown", "error": str(e), "status": "failed"}]


            for res in song_results:
                results.append((index, res))

    results.sort(key=lambda x: x[0])

    for idx, r in results:
        print(f"[{idx}/{total}] {r['title']}")

        if r["status"] == "failed":
            print("❌ Failed to process")
            print(f"   Reason: {r.get('error', 'Unknown error')}\n")
            continue

        if r["status"] == "partial":
            print("⚠️  BPM could not be detected")

        print("✅ Done\n")

        append_row(csv_path, [
            r["title"],
            r["filename"],
            r["samplerate"],
            f"{r['duration']:.2f}",
            f"{r['bpm']:.2f}",
            f"{r['bitrate']:.0f}",
            r["channels"],
            r["status"]
        ])
