#!/usr/bin/env python3
"""
fetch_transcript.py — Free YouTube transcript fetcher for the youtube-summarizer skill.

Dependencies (all free, no API key needed):
    pip install youtube-transcript-api yt-dlp

Usage:
    python3 fetch_transcript.py --url "https://www.youtube.com/watch?v=VIDEO_ID"

Output:
    Prints a JSON object to stdout with keys:
        video_id, title, channel, duration, transcript, language, status

    On error, prints JSON with status = "error" and a message field.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_metadata(video_id: str) -> dict:
    """Fetch video title, channel, and duration using yt-dlp (free, no API key)."""
    try:
        import subprocess
        result = subprocess.run(
            [
                "yt-dlp",
                "--dump-json",
                "--no-download",
                "--quiet",
                f"https://www.youtube.com/watch?v={video_id}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration_sec = data.get("duration", 0)
            minutes, seconds = divmod(int(duration_sec), 60)
            hours, minutes = divmod(minutes, 60)
            if hours:
                duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                duration_str = f"{minutes}:{seconds:02d}"
            return {
                "title": data.get("title", "Unknown Title"),
                "channel": data.get("uploader", data.get("channel", "Unknown Channel")),
                "duration": duration_str,
            }
    except Exception:
        pass

    return {
        "title": f"YouTube Video ({video_id})",
        "channel": "Unknown Channel",
        "duration": "Unknown",
    }


def fetch_transcript(video_id: str, prefer_lang: str = None) -> tuple[str, str]:
    """
    Fetch transcript text and the language it was fetched in.

    Returns: (transcript_text, language_code)
    Raises: RuntimeError on failure.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        raise RuntimeError(
            "youtube-transcript-api is not installed. Run: pip install youtube-transcript-api"
        )

    # New API requires instantiation
    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.list(video_id)
    except Exception as e:
        raise RuntimeError(f"Could not list transcripts: {e}")

    # Priority: preferred language → English → Arabic → any available
    priority_langs = []
    if prefer_lang:
        priority_langs.append(prefer_lang)
    priority_langs += ["en", "ar", "en-US", "ar-SA"]

    transcript = None
    used_lang = None

    # Try manual transcripts first, then auto-generated
    for lang in priority_langs:
        try:
            transcript = transcript_list.find_manually_created_transcript([lang])
            used_lang = lang
            break
        except Exception:
            continue

    if not transcript:
        for lang in priority_langs:
            try:
                transcript = transcript_list.find_generated_transcript([lang])
                used_lang = lang
                break
            except Exception:
                continue

    # Fall back to any available transcript
    if not transcript:
        try:
            available = list(transcript_list)
            if available:
                transcript = available[0]
                used_lang = transcript.language_code
        except Exception:
            pass

    if not transcript:
        raise RuntimeError(
            "No transcripts available for this video. "
            "The video may be private, age-restricted, or have no subtitles."
        )

    try:
        # New API: fetch() returns a FetchedTranscript object, iterate for text
        fetched = transcript.fetch()
        text = " ".join(entry.text for entry in fetched)
        # Clean up common transcript artifacts
        text = re.sub(r"\[.*?\]", "", text)       # Remove [Music], [Applause] etc.
        text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace
        return text, used_lang
    except Exception as e:
        raise RuntimeError(f"Failed to fetch transcript content: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube video transcript and metadata. Outputs JSON."
    )
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument(
        "--lang",
        default=None,
        help="Preferred transcript language code (e.g. en, ar). Optional.",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cached transcript and fetch fresh.",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        print(json.dumps({"status": "error", "message": f"Could not extract video ID from URL: {args.url}"}))
        sys.exit(1)

    # Check cache
    cache_file = CACHE_DIR / f"transcript_{video_id}.json"
    if cache_file.exists() and not args.no_cache:
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            cached["cached"] = True
            print(json.dumps(cached, ensure_ascii=False))
            return
        except Exception:
            pass  # Cache corrupted — re-fetch

    # Fetch metadata
    meta = fetch_metadata(video_id)

    # Fetch transcript
    try:
        transcript_text, lang_code = fetch_transcript(video_id, prefer_lang=args.lang)
    except RuntimeError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)

    result = {
        "status": "ok",
        "video_id": video_id,
        "title": meta["title"],
        "channel": meta["channel"],
        "duration": meta["duration"],
        "language": lang_code,
        "transcript": transcript_text,
        "cached": False,
    }

    # Write to cache
    try:
        cache_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass  # Caching is optional — don't fail because of it

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
