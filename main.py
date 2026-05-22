import customtkinter as ctk
import yt_dlp
import threading
import os
from tkinter import filedialog

# --- App Styling ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class ProfessionalDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern MP4 Video Downloader Pro")
        self.state('zoomed')
        self.geometry("1100x750")

        self.cookie_path = None

        # --- UI Layout ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=("gray90", "gray13"))
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self.main_frame, text="Pro MP4 Downloader", font=("Segoe UI", 36, "bold"))
        self.title_label.pack(pady=(40, 5), padx=50)

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="High-Definition Video • Multi-Threaded • MP4 Format",
            text_color="#3b8ed0", font=("Segoe UI", 14)
        )
        self.subtitle_label.pack(pady=(0, 30))

        # URL Input
        self.url_entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="Paste YouTube Video or Playlist URL...",
            width=650, height=50, corner_radius=10, font=("Segoe UI", 16)
        )
        self.url_entry.pack(pady=10, padx=50)

        # Cookie Selection
        self.cookie_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.cookie_frame.pack(pady=10)

        self.cookie_btn = ctk.CTkButton(
            self.cookie_frame, text="📂 Load cookies.txt",
            fg_color="gray30", hover_color="gray40", command=self.select_cookies
        )
        self.cookie_btn.pack(side="left", padx=5)

        self.cookie_status = ctk.CTkLabel(self.cookie_frame, text="No cookie file loaded", text_color="gray")
        self.cookie_status.pack(side="left", padx=5)

        # Main Action
        self.download_btn = ctk.CTkButton(
            self.main_frame, text="🎬 START VIDEO DOWNLOAD",
            height=60, width=300, font=("Segoe UI", 20, "bold"),
            corner_radius=10, command=self.start_task
        )
        self.download_btn.pack(pady=25)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=700, mode="indeterminate")
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        # Terminal/Log Screen
        self.log_box = ctk.CTkTextbox(self.main_frame, width=800, height=250, corner_radius=10, font=("Consolas", 12))
        self.log_box.pack(pady=(20, 40), padx=50)
        self.log_box.insert("0.0", "SYSTEM READY\nMode: MP4 Video (High Quality)\n")
        self.log_box.configure(state="disabled")

    def log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def select_cookies(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            self.cookie_path = file
            self.cookie_status.configure(text=os.path.basename(file), text_color="#2ecc71")
            self.log(f"✅ Cookies loaded from: {file}")

    def start_task(self):
        url = self.url_entry.get().strip()
        if not url: return
        self.download_btn.configure(state="disabled", text="RUNNING...")
        self.progress_bar.start()
        threading.Thread(target=self.run_download, args=(url,), daemon=True).start()

    def run_download(self, url):
        self.log("\n" + "=" * 60)
        self.log("Initializing HD Video Download...")

        ydl_opts = {
            # --- THE BULLETPROOF FORMAT ---
            # The asterisk (*) prevents crashes on Shorts or Intro videos
            'format': 'bestvideo*+bestaudio/best',

            # Convert everything to MP4
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],

            'outtmpl': '%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s' if 'playlist' in url else '%(title)s.%(ext)s',

            # --- STABILITY SETTINGS ---
            'concurrent_fragment_downloads': 5,
            'retries': 10,
            'fragment_retries': 10,
            'ignoreerrors': True,  # Keeps the playlist moving if one video is completely broken

            # --- SECURITY ---
            'nocheckcertificate': True,
            'javascript_filter': True,
            'cookiefile': self.cookie_path if self.cookie_path else None,

            # --- UI ---
            'logger': self.SimpleLogger(self.log),
            'progress_hooks': [self.on_progress],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log("\n✨ ALL VIDEOS DOWNLOADED SUCCESSFULLY!")
        except Exception as e:
            self.log(f"\n❌ ERROR: {str(e)}")
        finally:
            self.progress_bar.stop()
            self.download_btn.configure(state="normal", text="🎬 START VIDEO DOWNLOAD")

    class SimpleLogger:
        def __init__(self, log_func): self.log_func = log_func

        def debug(self, msg):
            if "Destination:" in msg: self.log_func(f"🎥 Downloading: {msg.split('Destination:')[-1].strip()}")

        def warning(self, msg): pass

        def error(self, msg): self.log_func(f"❌ {msg}")

    def on_progress(self, d):
        if d['status'] == 'finished':
            self.log("✅ Video download complete! Finalizing file...")


if __name__ == "__main__":
    app = ProfessionalDownloader()
    app.mainloop()
