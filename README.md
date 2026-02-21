# 🎵 S_CLOUD CLI

**S_CLOUD CLI** is a smart command-line tool that downloads music from SoundCloud, converts tracks to WAV format, analyzes audio metadata, and exports structured results to a CSV file.

It is designed for **music analysis, data collection, and audio research** workflows.

---

## ✨ Features

- 🔗 Accepts **SoundCloud track or playlist URLs**
- ⬇️ Downloads audio using `yt-dlp`
- 🎧 Converts audio to **WAV (48kHz)**
- 📊 Extracts:
  - Duration
  - Sample rate
  - Channels
  - Estimated BPM
  - Bitrate
- 📁 Organizes files automatically
- 📄 Exports all metadata to a **CSV file**
- ⚡ Multi-threaded processing
- 🧹 Automatic temporary file cleanup

---

## 📂 Project Structure

```
Sc/
├── main.py
├── data.csv
├── core/
    ├── controller.py
    ├── worker.py
    ├── metadata.py
    ├── csv_worker.py
    └── pars.py
```

---

## 🛠️ Requirements

### System Dependencies
FFmpeg must be installed and available in PATH.

### Python
Python 3.10+

---

## 📦 Installation

```bash
https://github.com/mloudifa/S_CLOUD-CLI.git
cd s_cloud_cli
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
python main.py
```

Enter a SoundCloud track or playlist URL when prompted.

---

## 📊 Output

- WAV files: `Songs/`
- Metadata CSV: `data.csv`

---

## 📄 License

MIT License
