#!/usr/bin/env python3
"""
build_word.py — the mechanical half of the make-english-word skill.

Takes a JSON payload describing one English word
and does all the file/network/subprocess work:
  1. Generates the illustrative image via Pollinations.ai (free, no key).
  2. Generates pronunciation + example audio via edge-tts.
  3. Renders the Obsidian note.

Usage:
    python3 build_word.py --json '<json string>'
    python3 build_word.py --json-file word.json

See SKILL.md for the JSON schema.

Image Generation: Pollinations.ai (free open-source, no API key needed)
"""

import argparse
import json
import subprocess
import sys
import urllib.request
import urllib.parse
from pathlib import Path

VOICE = "en-US-BrianNeural"


def generate_image(prompt: str, out_path: Path) -> None:
    """Generate image using multiple providers with automatic fallbacks."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Strategy: Pollinations.ai (free open-source, no key needed)
    print("[image] Generating via Pollinations.ai...", file=sys.stderr)
    generate_image_pollinations(prompt, out_path)


def generate_image_pollinations(prompt: str, out_path: Path) -> None:
    """Free fallback: generate image via Pollinations.ai (no API key needed)."""
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        with open(out_path, "wb") as f:
            f.write(response.read())
    print(f"[image] Pollinations.ai fallback succeeded", file=sys.stderr)


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
    examples_blocks = "\n\n".join(
        f"```text\n{line.strip()}\n```" for line in notes['common_examples'].strip().split("\n") if line.strip()
    )
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

### بالعامية المصرية
{notes['colloquial']}

### إمتى بتتقال؟
{notes['when_used']}

### أمثلة شائعة

{examples_blocks}

### مرادفات (Synonyms)

```text
{notes['synonyms']}
```

### أضداد (Antonyms)

```text
{notes['antonyms']}
```

### أخطاء شائعة
{notes['common_mistakes']}

### ملاحظات مهمة
{notes['important_notes']}

![[{word}.jpeg]]
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON payload as a string")
    parser.add_argument("--json-file", help="Path to a JSON file with the payload")
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

    images_dir = Path(payload["images_path"])
    pron_dir = Path(payload["pronunciation_path"])
    example_dir = Path(payload["examples_path"])
    words_dir = Path(payload["vocabulary_path"])

    image_path = images_dir / f"{word_cap}.jpeg"
    pron_path = pron_dir / f"{word_cap}_pronunciation.mp3"
    example_path = example_dir / f"{word_lower}_example.mp3"
    note_path = words_dir / f"{word_cap}.md"

    if note_path.exists() and not args.force:
        print(f"[skip] '{word_cap}' already exists at {note_path} — nothing generated.\n"
              f"       Pass --force to rebuild it anyway (this will regenerate the image and audio).")
        return 0

    print(f"[1/4] Generating image -> {image_path}")
    generate_image(payload["image_prompt"], image_path)

    print(f"[2/4] Generating pronunciation audio -> {pron_path}")
    generate_audio(word_cap, pron_path)

    print(f"[3/4] Generating example audio -> {example_path}")
    generate_audio(payload["example"], example_path)

    print(f"[4/4] Writing note -> {note_path}")
    words_dir.mkdir(parents=True, exist_ok=True)
    note_path.write_text(render_note(word_cap, payload), encoding="utf-8")

    print(f"\nDone: {word_cap}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
