#!/usr/bin/env python3
"""
build_word.py — the mechanical half of the make-english-word skill.

Takes a JSON payload describing one English word (already written by Claude)
and does all the file/network/subprocess work:
  1. Generates the illustrative image via Pollinations (free, no API key).
  2. Generates pronunciation + example audio via edge-tts.
  3. Renders the Obsidian note.
  4. Writes the Anki flashcard file.
  5. Copies the media files into the Anki collection.media folder.

Usage:
    python3 build_word.py --json '<json string>'
    python3 build_word.py --json-file word.json

See SKILL.md for the JSON schema.
"""

import argparse
import json
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_ANKI_MEDIA_DIR = "/home/nagdista/.local/share/Anki2/User 1/collection.media"
POLLINATIONS_BASE = "https://image.pollinations.ai/prompt/"
VOICE = "en-US-BrianNeural"

# Models to cycle through on retry. If the first (usually best) model is
# overloaded or returns a broken/tiny response, we fall back to the next one
# rather than failing the whole build. "flux" is Pollinations' default and
# generally the most accurate for detailed scene prompts like ours.
IMAGE_MODEL_FALLBACK_ORDER = ["flux", "turbo", "flux-realism"]

# A real generated JPEG is essentially never this small; a tiny response
# usually means an error page or placeholder got returned instead of an image.
MIN_VALID_IMAGE_BYTES = 5_000


def generate_image(prompt: str, out_path: Path, retries_per_model: int = 2) -> None:
    """Fetch an image from Pollinations for the given prompt.

    Tries each model in IMAGE_MODEL_FALLBACK_ORDER in turn. Within a model,
    retries a couple of times (transient network/queue issues). Moves to the
    next model if a given model keeps failing or keeps returning a
    suspiciously small/invalid response.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = urllib.parse.quote(prompt)

    last_err = None
    for model in IMAGE_MODEL_FALLBACK_ORDER:
        url = f"{POLLINATIONS_BASE}{encoded}?width=1024&height=1024&nologo=true&model={model}"
        for attempt in range(1, retries_per_model + 1):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "vocab-card-builder-skill"})
                with urllib.request.urlopen(req, timeout=90) as resp:
                    data = resp.read()
                if len(data) < MIN_VALID_IMAGE_BYTES:
                    raise RuntimeError(f"response too small ({len(data)} bytes) - likely not a real image")
                out_path.write_bytes(data)
                if model != IMAGE_MODEL_FALLBACK_ORDER[0]:
                    print(f"[image] succeeded using fallback model '{model}'", file=sys.stderr)
                return
            except Exception as e:  # noqa: BLE001 - want to retry/fallback on any transient failure
                last_err = e
                print(f"[image] model={model} attempt={attempt} failed: {e}", file=sys.stderr)
    raise RuntimeError(f"Image generation failed on all models/retries: {last_err}")



def generate_audio(text: str, out_path: Path, repeats: int = 5) -> None:
    """Generate an mp3 with edge-tts, speaking `text` `repeats` times."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    repeated = ". ".join([text] * repeats) + "."
    cmd = [
        "edge-tts",
        "--voice", VOICE,
        "--text", repeated,
        "--write-media", str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"edge-tts failed for {out_path}: {result.stderr}")


def render_note(word: str, fields: dict) -> str:
    notes = fields["notes"]
    return f"""---
char: {fields['char']}
type: {fields['type']}
status: {fields['status']}
image: {word}.jpeg
prompt: {fields['image_prompt']}
---

## {word} Info

| Word       | {word} |
| ---------- | ------ |
| Situation  | {fields['situation']} |
| Definition | {fields['definition']} |
| Example    | {fields['example']} |
| IPA        | `{fields['ipa']}` |

## {word} Pronunciation

![[{word}_pronunciation.mp3]]

## {word} Example

![[{word.lower()}_example.mp3]]

## {word} Notes

| العنصر | التفاصيل |
|--------|----------|
| بالعامية | {notes['colloquial']} |
| امتى بتتقال | {notes['when_used']} |
| أمثلة شائعة | {notes['common_examples'].replace(chr(10), '<br>')} |
| تركيب الجملة | {notes['sentence_structure']} |
| مرادفات | {notes['synonyms']} |
| antonyms | {notes['antonyms']} |
| أخطاء شائعة | {notes['common_mistakes']} |
| ملاحظات مهمة | {notes['important_notes']} |

![[{word}.jpeg]]
"""


def render_flashcard(word: str, example: str) -> str:
    word_lower = word.lower()
    front = f'<img src="{word}.jpeg" width="200"><br>{word}<br>[sound:{word}_pronunciation.mp3]'
    back = f"{example} [sound:{word_lower}_example.mp3]"
    return f"{front}\t{back}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON payload as a string")
    parser.add_argument("--json-file", help="Path to a JSON file with the payload")
    parser.add_argument("--vault-root", default=None, help="Override vault_root from the JSON")
    parser.add_argument("--anki-media-dir", default=DEFAULT_ANKI_MEDIA_DIR,
                         help="Path to the Anki collection.media folder")
    parser.add_argument("--skip-anki-copy", action="store_true",
                         help="Don't try to copy media into the Anki folder")
    parser.add_argument("--force", action="store_true",
                         help="Rebuild even if a note for this word already exists")
    args = parser.parse_args()

    if args.json:
        payload = json.loads(args.json)
    elif args.json_file:
        payload = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    else:
        parser.error("Provide --json or --json-file")

    word = payload["word"]
    word_cap = word[0].upper() + word[1:]
    word_lower = word.lower()
    vault_root = Path(args.vault_root or payload.get("vault_root", "English"))

    images_dir = vault_root / "Images"
    pron_dir = vault_root / "Listening" / "Pronunciation"
    example_dir = vault_root / "Listening" / "Examples"
    words_dir = vault_root / "Words"
    flashcards_dir = vault_root / "Flashcards"

    image_path = images_dir / f"{word_cap}.jpeg"
    pron_path = pron_dir / f"{word_cap}_pronunciation.mp3"
    example_path = example_dir / f"{word_lower}_example.mp3"
    note_path = words_dir / f"{word_cap}.md"
    flashcard_path = flashcards_dir / f"{word_cap}.txt"

    if note_path.exists() and not args.force:
        print(f"[skip] '{word_cap}' already exists at {note_path} — nothing generated.\n"
              f"       Pass --force to rebuild it anyway (this will regenerate the image and audio).")
        return 0

    print(f"[1/5] Generating image -> {image_path}")
    generate_image(payload["image_prompt"], image_path)

    print(f"[2/5] Generating pronunciation audio -> {pron_path}")
    generate_audio(word_cap, pron_path)

    print(f"[3/5] Generating example audio -> {example_path}")
    generate_audio(payload["example"], example_path)

    print(f"[4/5] Writing note -> {note_path}")
    words_dir.mkdir(parents=True, exist_ok=True)
    note_path.write_text(render_note(word_cap, payload), encoding="utf-8")

    print(f"[5/5] Writing flashcard -> {flashcard_path}")
    flashcards_dir.mkdir(parents=True, exist_ok=True)
    flashcard_path.write_text(render_flashcard(word_cap, payload["example"]), encoding="utf-8")

    if not args.skip_anki_copy:
        anki_dir = Path(args.anki_media_dir)
        if anki_dir.is_dir():
            for src in (image_path, pron_path, example_path):
                shutil.copy2(src, anki_dir / src.name)
            print(f"Copied media into Anki collection.media at {anki_dir}")
        else:
            print(f"[warn] Anki media dir not found at {anki_dir} — skipped copy. "
                  f"Pass --anki-media-dir to point at the real folder.", file=sys.stderr)

    print(f"\nDone: {word_cap}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
