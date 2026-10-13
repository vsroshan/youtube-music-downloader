YouTube Music Downloader

A Python command-line tool that automates finding, downloading, converting, and organizing song audio using YouTube search results.

Instead of manually searching for every song and copying individual video URLs, provide a text file containing artist and song names. The program searches YouTube, ranks candidate videos, downloads the selected audio, converts it to MP3, and organizes the output into artist-specific folders.

Features

* Batch song processing: Read a list of artist-song pairs from songs.txt.
* Automatic YouTube search: Search for songs using their artist and title.
* Candidate ranking: Use fuzzy text matching and keyword-based scoring to rank search results.
* Audio extraction: Download the selected video’s best available audio stream.
* MP3 conversion: Convert downloaded audio to MP3 using FFmpeg.
* Artist-based organization: Save songs in separate folders for each artist.
* Duplicate avoidance: Skip songs whose expected MP3 files already exist.
* ID3 metadata: Add song titles and artist names to MP3 files.
* Cover artwork: Attempt to embed a downloaded video thumbnail as cover art.
* Error handling: Report individual download failures while continuing through the song list.

How It Works

The program follows this workflow:

1. Reads artist-song pairs from songs.txt.
2. Searches YouTube for up to five candidate videos per song.
3. Scores candidates using fuzzy text matching and preferred or rejected keywords.
4. Selects the highest-scoring candidate.
5. Downloads the selected video’s audio.
6. Converts the audio to MP3 at the configured 192 kbps quality setting.
7. Organizes the resulting file into an artist-specific folder.
8. Adds title and artist metadata, and attempts to embed cover artwork.

Note: Candidate ranking is heuristic. The program does not independently verify the selected video’s audio content, and the highest-scoring result is not guaranteed to be the correct recording or an official upload.

Requirements

* Python 3
* yt-dlp
* rapidfuzz
* mutagen
* FFmpeg

FFmpeg is an external dependency used by yt-dlp for audio extraction and MP3 conversion. It must be installed separately and available to the application.

Installation

1. Clone the repository

git clone https://github.com/vsroshan/youtube-music-downloader.git
cd youtube-music-downloader

Replace YOUR-USERNAME with the GitHub username that owns this repository.

Alternatively, download the repository as a ZIP file from GitHub and extract it.

2. Create a virtual environment

Using a virtual environment helps keep the project’s Python dependencies separate from other applications.

On macOS or Linux:

python3 -m venv .venv
source .venv/bin/activate

On Windows:

py -m venv .venv
.venv\Scripts\activate

3. Install Python dependencies

If the repository includes requirements.txt, run:

python -m pip install -r requirements.txt

4. Install FFmpeg

Install FFmpeg using an appropriate method for your operating system.

On macOS, if Homebrew is installed:

brew install ffmpeg

On Windows or Linux, follow the installation instructions appropriate for your system.

Verify that FFmpeg is available:

ffmpeg -version

Preparing Your Song List

Create a file named songs.txt in the same working directory from which you run the program.

Use the following format:

Artist Name - Song Title
Another Artist - Another Song
Third Artist - Third Song

Each non-empty line must contain the artist name, followed by -, followed by the song title.

For example:

Daft Punk - Get Lucky
Coldplay - Yellow
Adele - Hello

The program processes the songs sequentially.

Lines that do not contain the expected separator are skipped.

Important: Use this example only as a formatting demonstration. Ensure that you have the necessary rights or permission to download any material you process.

Running the Program

Run the Python script:

python youtube_music_downloader.py

Replace youtube_music_downloader.py with the actual filename if it differs.

The program reads songs.txt, searches for each song, and prints progress and diagnostic messages in the terminal.

This is a command-line application; it does not currently provide a graphical user interface.

Output Structure

The program organizes downloaded MP3 files into artist-specific folders.

The current implementation uses this output location:

/Users/roshanvs/Downloads/output

The resulting directory structure may look like this:

output/
├── Daft Punk/
│   └── Get Lucky.mp3
├── Coldplay/
│   └── Yellow.mp3
└── Adele/
    └── Hello.mp3

These filenames are illustrative examples.

Configuration note: The output directory is hard-coded in the current source code. Users on other computers must change DOWNLOAD_ROOT to a suitable location before running the application.

Search Ranking

The program uses RapidFuzz to compare artist and song names against candidate video titles.

It also adjusts candidate scores using keyword lists.

Preferred keywords include:

* official audio
* official video
* topic
* vevo

Rejected keywords include:

* slowed
* reverb
* nightcore
* sped up
* bass boosted
* live
* remix
* fanmade
* cover
* karaoke

These keywords influence the score but do not guarantee that the selected video is correct.

Duplicate Handling

Before downloading a song, the program checks whether the expected MP3 file already exists.

If it exists, the program skips that song.

This avoids unnecessary repeat downloads when processing the same song list again.

Metadata and Cover Art

The program uses Mutagen to write ID3 metadata into downloaded MP3 files.

It attempts to set:

* Track title
* Artist name
* Cover artwork from the downloaded thumbnail, when a matching thumbnail file is found

Cover artwork embedding is best-effort. Some thumbnail formats or filename differences may prevent the artwork from being embedded correctly.

Troubleshooting

Python cannot find a required module

Activate your virtual environment and install the dependencies listed in requirements.txt.

Audio conversion fails

Confirm that FFmpeg is installed and available on your system.

The program cannot find songs.txt

Make sure the file exists in the working directory from which you launch the script.

Downloads are saved to the wrong location

Check the DOWNLOAD_ROOT setting in the Python source code and change it to a directory suitable for your computer.

The selected song is incorrect

The program ranks candidates using text-based heuristics. It does not verify the actual audio content, so manual review of search results may be necessary.

Cover artwork is missing

The program looks for a thumbnail file matching the cleaned song title. The thumbnail filename or format may differ from what the script expects.

Responsible Use

Use this application only for content you own, content you have permission to download, or content that is otherwise lawfully available for downloading.

Respect copyright, applicable laws, and YouTube’s terms and policies. Do not use this application to download copyrighted material without the necessary rights or authorization.

Project Status

This repository contains the initial published version of the project.

Author

Created as a personal Python programming project.
