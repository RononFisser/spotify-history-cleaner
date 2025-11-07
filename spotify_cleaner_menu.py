#!/usr/bin/env python3
"""
spotify_cleaner_menu_v2.py

Interactive menu to remove song or artist records across endsong_0.json–endsong_7.json.

- 1 = Remove by song keyword (loops until you go back)
- 2 = Remove by artist keyword (loops until you go back)
- 3 = Quit
"""

import json, glob, shutil, os, sys
from datetime import datetime

FILE_PREFIX = "endsong_"
FILE_COUNT = 8
SAMPLE_SHOW = 6

# --- Utility functions ---

def load_file(filename):
    """Load JSON array or NDJSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"  Error opening {filename}: {e}")
        return None, None

    # Try array first
    try:
        arr = json.loads(text)
        if isinstance(arr, list):
            return arr, "array"
    except Exception:
        pass

    # Try NDJSON
    try:
        objs = [json.loads(line) for line in text.splitlines() if line.strip()]
        return objs, "ndjson"
    except Exception as e:
        print(f"  JSON error in {filename}: {e}")
        return None, None


def write_file(filename, data, mode):
    """Write JSON data back in same format."""
    try:
        if mode == "array":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                for entry in data:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return True
    except Exception as e:
        print(f"  Error writing {filename}: {e}")
        return False


def ensure_backup(filename):
    """Create a backup of the file before overwriting."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = f"{filename}.bak.{timestamp}"
    try:
        shutil.copy2(filename, bak)
        return bak
    except Exception as e:
        print(f"  Could not create backup for {filename}: {e}")
        return None


def get_file_list():
    """Get all endsong_*.json files."""
    files = []
    for i in range(FILE_COUNT):
        fname = f"{FILE_PREFIX}{i}.json"
        if os.path.exists(fname):
            files.append(fname)
    if not files:
        files = sorted(glob.glob("endsong_*.json"))
    return files


def sample_display(entries):
    """Show sample of matched entries."""
    for i, e in enumerate(entries[:SAMPLE_SHOW]):
        ts = e.get("ts") or e.get("endTime") or "(no time)"
        artist = e.get("master_metadata_album_artist_name") or e.get("artistName") or ""
        title = e.get("master_metadata_track_name") or e.get("trackName") or ""
        print(f"   {i+1}. {ts} | {artist} – {title}")


def match_entry(entry, keyword, by_artist=False):
    field = (entry.get("master_metadata_album_artist_name") if by_artist else entry.get("master_metadata_track_name"))
    field = field or entry.get("artistName") if by_artist else entry.get("trackName")
    if not field:
        return False
    return keyword.lower() in field.lower()


def clean_files(keyword, by_artist=False):
    """Remove entries matching keyword across all endsong_*.json files."""
    files = get_file_list()
    if not files:
        print("No endsong_*.json files found in current directory.")
        return

    total_removed = 0
    total_matches = 0

    print(f"\nScanning for {'artist' if by_artist else 'song'} keyword: '{keyword}'")

    for filename in files:
        data, mode = load_file(filename)
        if data is None:
            continue

        matches = [e for e in data if match_entry(e, keyword, by_artist)]
        if not matches:
            continue

        print(f"\nFile: {filename} — {len(matches)} matches found:")
        sample_display(matches)

        confirm = input(f"Remove these {len(matches)} entries from {filename}? (y/n): ").strip().lower()
        if confirm != "y":
            print("  Skipped.")
            continue

        backup = ensure_backup(filename)
        if backup:
            print(f"  Backup saved as {backup}")

        filtered = [e for e in data if not match_entry(e, keyword, by_artist)]
        write_file(filename, filtered, mode)
        removed = len(data) - len(filtered)
        print(f"  Removed {removed} entries from {filename}")
        total_removed += removed
        total_matches += len(matches)

    if total_removed > 0:
        print(f"\nDone! Removed {total_removed} entries across all files.")
    elif total_matches == 0:
        print("\nNo matching entries found.")
    else:
        print("\nNo changes were made (all skipped).")


# --- Menu system ---

def run_removal_loop(by_artist=False):
    """Loop for repeated deletions of the same type."""
    mode = "artist" if by_artist else "song"
    while True:
        print(f"\n--- Remove by {mode} mode ---")
        print("Type a keyword to remove or 'back' to return to main menu.")
        keyword = input(f"Enter {mode} keyword: ").strip()
        if keyword.lower() == "back":
            print("Returning to main menu...")
            break
        elif not keyword:
            print("Please enter a valid keyword.")
            continue
        clean_files(keyword, by_artist)


def menu():
    """Main menu loop."""
    while True:
        print("\n=== Spotify History Cleaner ===")
        print("1) Remove by SONG keyword")
        print("2) Remove by ARTIST keyword")
        print("3) Quit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            run_removal_loop(by_artist=False)
        elif choice == "2":
            run_removal_loop(by_artist=True)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    if sys.version_info < (3, 6):
        print("Please use Python 3.6 or newer.")
        sys.exit(1)
    menu()
