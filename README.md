# AnderOng TTS

A lightweight, clean, and intuitive Text-to-Speech (TTS) desktop application built with Python. It leverages Microsoft Edge's advanced neural text-to-speech engine via `edge-tts` to generate highly natural, human-like voiceovers in multiple languages.

Designed specifically for quick voice script generations, it's perfect for Interactive Voice Response (IVR) systems, automated announcements, or general narration tasks.

---

## ✨ Features

* **Multi-Language Support**: One-click selection for **English**, **Malay**, and **Chinese** voice synthesis.
* **Gender Variants**: Switch seamlessly between natural-sounding **Female** and **Male** neural voices for each language.
* **Precise Speed Adjustment**: Fine-tune the narration speed using an intuitive slider ranging from `-50%` to `+50%` with real-time percentage feedback.
* **Threaded Performance**: The core speech synthesis engine runs asynchronously on a background thread, ensuring the User Interface (UI) remains snappy and never freezes during long audio processing.
* **Zero Dependencies for End Users**: Can be compiled into a standalone, single-executable (`.exe`) file that runs instantly without installing Python or external runtimes.

---

## 🛠️ Tech Stack & Credits

* **GUI Framework**: Python Built-in `tkinter` (with `ttk` clam theme for a clean aesthetic).
* **TTS Core Engine**: `edge-tts` (Microsoft Edge Neural Voices).
* **Concurrency**: `asyncio` + `threading` wrapper.
* **Packaging Tool**: `PyInstaller`.

---

## 🚀 How to Run (Development)

### Prerequisites
Make sure you have Python 3.10+ installed.

### Installation
1. Clone this repository or download the source files.
2. Install the required dependencies:
```bash
   pip install edge-tts pyinstaller
