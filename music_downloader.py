import re
from pathlib import Path

from rapidfuzz import fuzz
from mutagen.id3 import APIC, ID3, TPE1, TIT2
from mutagen.mp3 import MP3
import yt_dlp


# =========================
# SETTINGS
# =========================

SONG_LIST_FILE = "songs.txt"

DOWNLOAD_ROOT = "/Users/roshanvs/Downloads/output"

AUDIO_QUALITY = 192


MAX_RESULTS = 5

# Reject these keywords
BAD_KEYWORDS = [
    "slowed",
    "reverb",
    "nightcore",
    "sped up",
    "bass boosted",
    "live",
    "remix",
    "fanmade",
    "cover",
    "karaoke"
]

# Prefer these
GOOD_KEYWORDS = [
    "official audio",
    "official video",
    "topic",
    "vevo"
]

# =========================
# HELPERS
# =========================

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def score_video(title, artist, song):
    title_lower = title.lower()

    score = 0

    # Strong artist/song match
    score += fuzz.partial_ratio(artist.lower(), title_lower)
    score += fuzz.partial_ratio(song.lower(), title_lower)

    # Prefer official uploads
    for good in GOOD_KEYWORDS:
        if good in title_lower:
            score += 20

    # Reject garbage uploads
    for bad in BAD_KEYWORDS:
        if bad in title_lower:
            score -= 50

    return score

# =========================
# DOWNLOAD SONG
# =========================

def download_song(artist, song):

    artist_folder = Path(DOWNLOAD_ROOT) / clean_filename(artist)
    artist_folder.mkdir(parents=True, exist_ok=True)

    final_mp3 = artist_folder / f"{clean_filename(song)}.mp3"

    # Skip existing
    if final_mp3.exists():
        print(f"Skipping existing: {song}")
        return

    query = f"{artist} {song}"

    print(f"\nSearching: {query}")

    search_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(search_opts) as ydl:
        results = ydl.extract_info(
            f"ytsearch{MAX_RESULTS}:{query}",
            download=False
        )

    entries = results.get("entries", [])

    if not entries:
        print("No results found")
        return

    # Pick best match
    best_video = None
    best_score = -999

    for entry in entries:
        title = entry.get("title", "")

        current_score = score_video(title, artist, song)

        print(f"Candidate: {title}")
        print(f"Score: {current_score}")

        if current_score > best_score:
            best_score = current_score
            best_video = entry

    if not best_video:
        print("No suitable video found")
        return

    video_url = f"https://www.youtube.com/watch?v={best_video['id']}"

    print(f"Downloading: {best_video['title']}")

    temp_output = artist_folder / clean_filename(song)

    ydl_opts = {
        'format': 'bestaudio/best',
        # Use a template so yt-dlp writes deterministic filenames.
        # Keep noplaylist=True; outtmpl controls the final base filename.
        'outtmpl': str(temp_output),

        'quiet': False,
        'noplaylist': True,
        'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': AUDIO_QUALITY,
            }
        ],
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Find generated mp3 (yt-dlp naming can vary; use the newest matching mp3)
    cleaned_song = clean_filename(song)
    mp3_candidates = sorted(
        [p for p in artist_folder.glob(f"{cleaned_song}*.mp3") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not mp3_candidates:
        # Fallback: any mp3 in the folder (newest)
        all_mp3s = sorted(
            [p for p in artist_folder.glob("*.mp3") if p.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not all_mp3s:
            print("MP3 not found after download")
            return
        generated_mp3 = all_mp3s[0]
    else:
        generated_mp3 = mp3_candidates[0]

    # Find thumbnail
    thumbnail = None
    thumbnail_mime = None

    ext_to_mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }

    for ext in ["jpg", "jpeg", "webp", "png"]:
        possible = artist_folder / f"{cleaned_song}.{ext}"
        if possible.exists():
            thumbnail = possible
            thumbnail_mime = ext_to_mime.get(ext)
            break


    # Embed metadata
    try:
        audio = MP3(generated_mp3, ID3=ID3)

        try:
            audio.add_tags()
        except:
            pass

        audio.tags.add(TIT2(
            encoding=3,
            text=song
        ))

        audio.tags.add(TPE1(
            encoding=3,
            text=artist
        ))

        if thumbnail:
            with open(thumbnail, 'rb') as img:
                audio.tags.add(
                    APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=img.read()
                    )
                )

        audio.save()

        print("Metadata added")

    except Exception as e:
        print("Metadata failed:", e)

# =========================
# MAIN
# =========================

def main():

    with open(SONG_LIST_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:

        if " - " not in line:
            print(f"Invalid format: {line}")
            continue

        artist, song = line.split(" - ", 1)

        try:
            download_song(artist.strip(), song.strip())
        except Exception as e:
            print(f"Failed: {line}")
            print(e)

if __name__ == "__main__":
    main()