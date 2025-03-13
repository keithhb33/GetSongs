# YouTube MP3/MP4 Downloader

A Windows desktop app that downloads YouTube videos or extracts audio as MP3 – **no ffmpeg required**. Built in Python using **Tkinter** for a simple GUI, packaged as a single `.exe` with [PyInstaller](https://www.pyinstaller.org/).

## Table of Contents

- [Features](#features)  
- [Screenshots](#screenshots)  
- [How It Works](#how-it-works)  
- [Usage](#usage)  
  - [Running the Source Python Script](#running-the-source-python-script)  
  - [Using the Standalone EXE](#using-the-standalone-exe)  
- [Settings Persistence](#settings-persistence)  
- [Building the EXE](#building-the-exe)  
  - [Dependencies](#dependencies)  
  - [PyInstaller Command](#pyinstaller-command)  
  - [Common Issues](#common-issues)  
- [Security & Antivirus Warnings](#security--antivirus-warnings)  
- [License](#license)

---

## Features

1. **Download Videos** as MP4 in the highest available resolution.  
2. **Extract Audio** as MP3 by simply renaming the audio-only file (no ffmpeg needed).  
3. **Remembers Download Folder** across sessions (stores `settings.json` next to the `.exe` or in the script directory).  
4. **Simple GUI** with no console window.  
5. **Packaged as a Single Executable** using PyInstaller, so you can run it on most Windows machines without installing Python.

---

## Screenshots

*(Add screenshots of your GUI here!)*

<p align="center">
  <img src="path/to/screenshot.png" alt="YouTube Downloader Screenshot" width="400">
</p>

---

## How It Works

1. **User enters a YouTube URL** and selects a download format (MP4 or MP3).  
2. **App fetches metadata** via [`pytubefix`](#) (a forked or local version of PyTube).  
3. **MP4 Download**: The highest-resolution video+audio stream is saved.  
4. **MP3 Download**: An audio-only stream is downloaded, then the file extension is renamed from `.mp4` (or `.m4a`) to `.mp3`.   
   - *(In most players, this is enough to play the track. If you need a true MP3 container, consider using ffmpeg to convert instead.)*

---

## Usage

### Running the Source Python Script

1. **Clone** the repository or download the files to your local machine.
2. **Install dependencies** in a virtual environment:
   ```bash
   pip install -r requirements.txt
