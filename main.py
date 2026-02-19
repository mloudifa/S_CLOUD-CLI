from core.csv_worker import init_csv
from core.controller import run_pipeline
from core.metadata import fetch_metadata

import os
import shutil
import sys
import time


# ========= CLI UX ========= #

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print(r'r'"""
███████╗ ██████╗██╗      ██████╗ ██╗   ██╗██████╗ 
██╔════╝██╔════╝██║     ██╔═══██╗██║   ██║██╔══██╗
███████╗██║     ██║     ██║   ██║██║   ██║██║  ██║
╚════██║██║     ██║     ██║   ██║██║   ██║██║  ██║
███████║╚██████╗███████╗╚██████╔╝╚██████╔╝██████╔╝
╚══════╝ ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ 

            🎵  S_CLOUD CLI  🎵
    ----------------------------------
      Smart Cloud Music Analyzer
    """)


def status(msg):
    print(f"➡️  {msg}")
    time.sleep(0.4)  # small UX delay (not required)


# ========= MAIN ========= #

def main():
    clear()
    banner()

    print("\nWelcome to S_CLOUD CLI 🚀\n")

    url = input("🔗 Enter playlist / album / track URL → ").strip()

    if not url:
        print("\n❌ No URL provided. Exiting.")
        sys.exit(1)

    status("Analyzing URL and fetching metadata...")
    songs = fetch_metadata(url)

    if not songs:
        print("\n❌ No songs found or invalid URL.")
        sys.exit(1)

    OUTPUT_DIR = os.path.join(os.getcwd(), "Songs")
    CSV_PATH = os.path.join(os.getcwd(), "data.csv")

    status("Initializing CSV file...")
    init_csv(CSV_PATH)

    status("Running processing pipeline...")
    run_pipeline(songs, OUTPUT_DIR, CSV_PATH)

    tmp_path = os.path.join(OUTPUT_DIR, "tmp")
    if os.path.exists(tmp_path):
        status("Cleaning temporary files...")
        shutil.rmtree(tmp_path)

    print("\n🎉 All done successfully!")
    print(f"📁 Songs directory: {OUTPUT_DIR}")
    print(f"📊 CSV file: {CSV_PATH}")
    print("\nThanks for using S_CLOUD CLI 💙\n")


if __name__ == "__main__":
    main()
