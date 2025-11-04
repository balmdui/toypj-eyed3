import re
from pathlib import Path
import eyed3


def edit_mp3_tags(directory, cover_art_path):
    """
    Edit MP3 file tags using eyed3 library.

    Sets:
    - artist: 조용필
    - album: 이순간영원히
    - title: {filename without .mp3}
    - recording_date: 2025
    - cover art: from provided image file
    """
    directory_path = Path(directory).expanduser()
    cover_path = Path(cover_art_path).expanduser()

    if not directory_path.exists():
        print(f"Directory not found: {directory_path}")
        return

    if not cover_path.exists():
        print(f"Cover art file not found: {cover_path}")
        return

    # Get all MP3 files
    mp3_files = list(directory_path.glob("*.mp3"))

    if not mp3_files:
        print("No MP3 files found in the directory.")
        return

    print(f"Found {len(mp3_files)} MP3 files\n")

    # Read cover art data
    with open(cover_path, 'rb') as cover_file:
        cover_data = cover_file.read()

    # Determine image MIME type
    cover_ext = cover_path.suffix.lower()
    mime_type = 'image/jpeg' if cover_ext in ['.jpg', '.jpeg'] else 'image/png'

    for file_path in mp3_files:
        try:
            # Load the MP3 file
            audiofile = eyed3.load(file_path)

            if audiofile is None:
                print(f"✗ Could not load: {file_path.name}\n")
                continue

            # Initialize tag if it doesn't exist
            if audiofile.tag is None:
                audiofile.initTag()

            # Get title from filename (without .mp3 extension)
            title = file_path.stem

            # Set tags
            audiofile.tag.artist = "조용필"
            audiofile.tag.album = "이순간을영원히"
            audiofile.tag.title = title
            audiofile.tag.recording_date = "2025"

            # Clear existing images and add new cover art
            audiofile.tag.images.remove("")
            audiofile.tag.images.set(3, cover_data, mime_type, "Cover")

            # Save the changes
            audiofile.tag.save()

            print(f"✓ Tagged: {file_path.name}")
            print(f"   Title: {title}")
            print(f"   Artist: 조용필")
            print(f"   Album: 이순간을영원히")
            print(f"   Year: 2025\n")

        except Exception as e:
            print(f"✗ Error tagging {file_path.name}: {e}\n")


def rename_mp3_files(directory):
    """
    Rename MP3 files to extract just the song title.

    Example:
    "조용필 - Bounce [광복80주년 KBS대기획 - 조용필, 이 순간을 영원히] ｜ KBS 251006 방송.mp3"
    becomes "Bounce.mp3"
    """
    directory_path = Path(directory).expanduser()

    if not directory_path.exists():
        print(f"Directory not found: {directory_path}")
        return

    # Get all MP3 files
    mp3_files = list(directory_path.glob("*.mp3"))

    if not mp3_files:
        print("No MP3 files found in the directory.")
        return

    print(f"Found {len(mp3_files)} MP3 files\n")

    for file_path in mp3_files:
        old_name = file_path.name

        # Extract title between "조용필 - " and " [" or "｜"
        # Pattern: artist - title [extra info] | more info.mp3
        match = re.search(r'조용필\s*-\s*(.+?)\s*[\[｜]', old_name)

        if match:
            title = match.group(1).strip()
            new_name = f"{title}.mp3"
            new_path = file_path.parent / new_name

            # Check if target file already exists
            if new_path.exists():
                print(f"⚠️  Skip: {new_name} already exists")
                continue

            try:
                file_path.rename(new_path)
                print(f"✓ Renamed: {old_name}")
                print(f"       to: {new_name}\n")
            except Exception as e:
                print(f"✗ Error renaming {old_name}: {e}\n")
        else:
            print(f"⚠️  Could not extract title from: {old_name}\n")


def main():
    music_dir = "~/Music/choyongpil"
    cover_art = "~/dev/toypj-eyed3/이순간을영원히.jpg"

    print("MP3 File Manager")
    print("=" * 60)
    print(f"Directory: {music_dir}")
    print(f"Cover Art: {cover_art}\n")

    print("Options:")
    print("1. Rename files (remove extra text, keep only song title)")
    print("2. Edit MP3 tags (artist, album, title, year, cover art)")
    print("3. Do both (rename first, then edit tags)")
    print("4. Exit\n")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        response = input("\nProceed with renaming files? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            rename_mp3_files(music_dir)
            print("\nDone!")
        else:
            print("Cancelled.")

    elif choice == "2":
        response = input("\nProceed with editing MP3 tags? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            edit_mp3_tags(music_dir, cover_art)
            print("\nDone!")
        else:
            print("Cancelled.")

    elif choice == "3":
        response = input("\nProceed with renaming and tagging? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            print("\n--- Step 1: Renaming Files ---")
            rename_mp3_files(music_dir)
            print("\n--- Step 2: Editing Tags ---")
            edit_mp3_tags(music_dir, cover_art)
            print("\nAll done!")
        else:
            print("Cancelled.")

    elif choice == "4":
        print("Exiting.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
