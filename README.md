# MP4 YouTube Downloader

## 📌 Project Overview
A modern, dark-themed, multi-threaded desktop desktop application built using Python to extract high-definition videos and playlists safely and quickly.

## 🛠️ Tech Stack & Architecture
- **GUI Engine:** `customtkinter` & `tkinter` (Modern UI architecture)
- **Download Engine:** `yt_dlp` (Asynchronous streaming wrapper)
- **Concurrency:** `threading` (Prevents application UI freezing during network operations)

## ⚡ Key Features & Security Enhancements
- **Multi-Threading:** Download logic runs asynchronously, keeping the window responsive.
- **Fail-Safe Playlists:** Enabled `ignoreerrors` flags to skip broken video URLs without halting the queue.
- **Adaptive Resolution Matrix:** Enforces `bestvideo*+bestaudio/best` rules to stabilize parsing on short-form contents.
- **Cookie Authentication Bypass:** Includes localized loading systems for secure cookie streams.

## 🚀 Installation & Running
Ensure you have Python installed, then run:
```bash
pip install customtkinter yt-dlp
python main.py
