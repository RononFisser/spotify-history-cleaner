==================== README.md ====================
# Spotify History Cleaner

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()
[![GitHub Repo](https://img.shields.io/badge/github-RononFisser%2Fspotify--history--cleaner-black?logo=github)]()

A Python tool by [@RononFisser](https://github.com/RononFisser) that lets you clean unwanted songs or artists from your Spotify streaming history before importing it into Stats.fm.

This script provides a simple interactive menu where you can:
- Remove all entries for a specific song or artist
- Preview matches before deleting
- Automatically back up every modified file
- Clean multiple keywords quickly
- Safely edit all `endsong_0.json` → `endsong_7.json` files from your Spotify export

## Features

- Interactive, user-friendly menu
- Case-insensitive, partial keyword matching
- Works across multiple Spotify JSON files
- Automatic backup before each edit
- Fully offline — no data leaves your computer

## Requirements

- Python 3.6 or later
- Spotify streaming history files named:
  ```
  endsong_0.json, endsong_1.json, ..., endsong_7.json
  ```
  (You can export these from https://www.spotify.com/account/privacy/)

## Usage

1. Place this script in the same folder as your Spotify history files.
2. Open a terminal in that folder.
3. Run:
   ```bash
   python spotify_cleaner_menu_v2.py
   ```
4. Follow the on-screen options:
   - 1: Remove by song keyword
   - 2: Remove by artist keyword
   - 3: Quit
   - Type `back` to return to the menu from a mode.

## Example Session

```
=== Spotify History Cleaner ===
1) Remove by SONG keyword
2) Remove by ARTIST keyword
3) Quit
Choose an option (1/2/3): 2

--- Remove by artist mode ---
Type a keyword to remove or 'back' to return to main menu.
Enter artist keyword: taylor swift

Scanning for artist keyword: 'taylor swift'
File: endsong_0.json — 15 matches found:
   1. 2020-07-28T18:53:42Z | Taylor Swift – Blank Space
...
Remove these 15 entries from endsong_0.json? (y/n): y
  Backup saved as endsong_0.json.bak.20251107_203402
  Removed 15 entries from endsong_0.json
```

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

Created by [@RononFisser](https://github.com/RononFisser)  
For anyone who wants to keep their Spotify stats clean and accurate.