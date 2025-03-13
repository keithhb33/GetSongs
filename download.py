import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from pytubefix import YouTube
except ImportError:
    messagebox.showerror("Error", "pytubefix is not installed or not found.")
    sys.exit(1)

# ------------------------------------------------------------------------------
# Distinguish between running from .py vs. running as a frozen .exe
# ------------------------------------------------------------------------------
FROZEN = getattr(sys, 'frozen', False)

if FROZEN:
    # Running inside PyInstaller .exe
    ASSETS_DIR = sys._MEIPASS  # Where embedded files (like dj.ico) are unpacked
    APP_DIR = os.path.dirname(sys.executable)  # Folder containing the .exe
else:
    # Running from source .py
    ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = ASSETS_DIR

CONFIG_FILE = os.path.join(APP_DIR, "settings.json")

# ------------------------------------------------------------------------------
# Load config (last save directory) or default to current directory
# ------------------------------------------------------------------------------
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("save_directory", os.getcwd())
        except:
            pass
    return os.getcwd()

# ------------------------------------------------------------------------------
# Save config
# ------------------------------------------------------------------------------
def save_config(directory):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"save_directory": directory}, f, indent=2)
    except Exception as e:
        print(f"Could not save config: {e}")

# Global variable for the folder
save_directory = load_config()

# ------------------------------------------------------------------------------
# Let user pick the folder; store in JSON for future runs
# ------------------------------------------------------------------------------
def choose_directory():
    global save_directory
    folder = filedialog.askdirectory(
        title="Select Save Location",
        initialdir=save_directory
    )
    if folder:
        save_directory = folder
        save_entry_var.set(save_directory)
        save_config(save_directory)

# ------------------------------------------------------------------------------
# Download function (pytubefix)
# ------------------------------------------------------------------------------
def download_video():
    url = url_entry.get().strip()
    fmt = format_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    try:
        yt = YouTube(url)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load video:\n{e}")
        return

    try:
        if fmt == "MP4":
            # Highest resolution
            stream = yt.streams.get_highest_resolution()
            out_file = stream.download(output_path=save_directory)
            messagebox.showinfo("Success", f"Video downloaded:\n{out_file}")

        elif fmt == "MP3":
            # Audio-only; rename to .mp3
            stream = yt.streams.filter(only_audio=True).first()
            if not stream:
                messagebox.showerror("Error", "No audio stream available.")
                return

            out_file = stream.download(output_path=save_directory)
            base, _ = os.path.splitext(out_file)
            new_file = base + ".mp3"
            os.rename(out_file, new_file)
            messagebox.showinfo("Success", f"Audio downloaded as MP3:\n{new_file}")

        else:
            messagebox.showerror("Error", "Invalid format selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

# ------------------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------------------
root = tk.Tk()
root.title("YouTube Downloader")
root.resizable(False, False)

# Load the embedded icon from inside the exe
icon_path = os.path.join(ASSETS_DIR, "dj.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print("Icon file not found:", icon_path)

# Nice theme if available
style = ttk.Style(root)
if "vista" in style.theme_names():
    style.theme_use("vista")
elif "winnative" in style.theme_names():
    style.theme_use("winnative")

header = ttk.Label(root, text="YouTube Downloader", font=("Segoe UI", 16, "bold"))
header.grid(row=0, column=0, columnspan=3, padx=10, pady=(15, 10))

# URL
ttk.Label(root, text="YouTube URL:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

# Format
ttk.Label(root, text="Format:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
format_var = tk.StringVar(value="MP3")
format_dropdown = ttk.Combobox(
    root,
    textvariable=format_var,
    values=["MP4", "MP3"],
    state="readonly",
    width=10
)
format_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Save Location
ttk.Label(root, text="Save Location:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
save_entry_var = tk.StringVar(value=save_directory)
save_entry = ttk.Entry(root, textvariable=save_entry_var, width=40, state="readonly")
save_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

browse_button = ttk.Button(root, text="Browse...", command=choose_directory)
browse_button.grid(row=3, column=2, padx=10, pady=10, sticky="w")

# Download Button
download_button = ttk.Button(root, text="Download", command=download_video, width=20)
download_button.grid(row=4, column=0, columnspan=3, padx=10, pady=(20, 15))

root.mainloop()
