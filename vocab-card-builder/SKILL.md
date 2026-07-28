---
name: vocab-card-builder
description: Build a complete English vocabulary learning card for a single English word, phrase, or idiom — an Obsidian note (definition, situation, example, IPA, Egyptian-dialect notes), an AI-generated illustrative image, pronunciation and example audio via edge-tts, and an AnkiDroid flashcard file, all saved into the user's vault and Anki media folder automatically. Use this skill whenever the user gives an English word and wants it "made" or "added" — e.g. "اعمل كلمة abandon", "make english word procrastinate", "ضيفلي vocab card لكلمة X", or any request to turn a new English word/phrase/idiom into a full study card with image + audio + flashcard.
---

# Vocab Card Builder

This skill turns one English word (or phrase/idiom) into a complete, ready-to-study package: an Obsidian note, an image that *is* the example sentence, two audio files, and an Anki flashcard — with zero manual steps from the user afterward.

The mechanical work (calling the image API, calling edge-tts, writing files, copying media into Anki) is handled by `scripts/build_word.py`. Your job is the part that needs judgment: writing the content that goes into that script.

## Step 0 — Check if this word already exists

Before writing anything, check whether the word already has a note:

```bash
ls "{vault_root}/Words/{Word}.md" 2>/dev/null
```

(`{Word}` = first letter capitalized, e.g. `Abandon`; `{vault_root}` defaults to `English` — use whatever value the user has been using in this vault.)

- **If it exists**: tell the user the word already has a card, show them the existing note's Definition/Example so they can see what's there, and ask whether they want to rebuild it (pass `--force` in Step 4) or leave it as is. Don't regenerate the image/audio unless they confirm — image and audio generation cost time and, in the case of the image, a queued request on a shared free service, so redoing it without being asked is wasteful.
- **If it doesn't exist**: proceed to Step 1 normally.

## Step 1 — Write the content

For the given word, produce these fields yourself. Take your time here — this is the part a script can't do, and the quality of the whole card depends on it.

| Field | What it is | Rules |
|---|---|---|
| `char` | First letter of the word | Uppercase |
| `type` | Noun / Verb / Phrase / Idiom / Adjective / ... | Pick the one that fits how the word is being taught |
| `status` | Difficulty tag | Default to `Hard` unless the user says otherwise |
| `ipa` | IPA transcription | Always the base/root form, never the conjugated form (e.g. `abandon`, not `abandoned`) |
| `definition` | Plain English definition | One sentence, simple |
| `situation` | A short narrative scene in English showing the word's meaning through context | Third person, a little story — this is what the image will be built from |
| `example` | A short, memorable example sentence in English | Written in the user's own voice, as if *they* are saying it to someone — never on behalf of a third character. Keep it short and simple, not literary. **The image must depict exactly this sentence — the example and the image are one and the same thing, not two separate ideas.** |
| `notes` | A small table in Egyptian Arabic dialect | See sub-fields below |

`notes` sub-fields (all in Egyptian Arabic, casual and practical — this is the part that makes the word actually stick for an Egyptian learner):
- `colloquial` — إيه أقرب معنى بالعامي المصري
- `when_used` — امتى الكلمة دي بتتقال في كلام عادي
- `common_examples` — 2-3 جمل تانية غير المثال الأساسي (مع ترجمة لو محتاجة)
- `sentence_structure` — تركيب الجملة (إيه اللي بييجي بعد الكلمة عادة)
- `synonyms` — مرادفات إنجليزي
- `antonyms` — أضداد إنجليزي
- `common_mistakes` — الأخطاء الشائعة اللي المصريين بيقعوا فيها مع الكلمة دي
- `important_notes` — أي حاجة تانية مهمة (نبرة الكلمة، سياقها العاطفي، إلخ)

## Step 2 — Build the image prompt

Write one `image_prompt` string. It **must** follow this exact shape:

1. Start with: `the word is {Word}, square image, 1:1 aspect ratio.`
2. Then a detailed visual description of the **situation/example** as a real scene — people, expressions, atmosphere, colors, location, small details. **Set it in everyday Egyptian life** (a Cairo street, a Metro carriage, a baladi apartment, a coffeeshop, a microbus, a university lecture hall, etc.) so the imagery feels familiar and personal rather than generic stock-photo Western imagery.
3. End with: `write the word {Word} in English text centered at the top middle of the image`

The prompt is not a caption for the example — it *is* the example, rendered as a scene. See `references/example_abandon.md` for a full worked example of this end-to-end.

## Step 3 — Show a preview and wait for approval

**Don't call the build script yet.** Image generation takes real time and hits a shared free service, and audio generation runs a local TTS process — both are wasteful to redo just because a word choice or scene detail didn't land. Show the user, as plain chat text (no file, no image yet):

- The **Example** sentence
- The **Situation**
- The full **image_prompt** you built in Step 2
- A one-line summary of the Arabic notes (just `colloquial` + `when_used` is enough for a quick sanity check — no need to dump the whole table)

Then ask something like: "الوصف ده تمام كده، ولا فيه حاجة عايز تغيرها قبل ما أولد الصورة والصوت؟"

- If the user approves (or doesn't reply with changes), move to Step 4.
- If they ask for changes, revise the relevant field(s) and show the preview again — don't generate anything until they're happy with it.

## Step 4 — Run the build script

Once the user has approved the content, call the build script — it does everything else:

```bash
python3 scripts/build_word.py --json '<the JSON below>'
```

JSON shape:

```json
{
  "word": "Abandon",
  "char": "A",
  "type": "Verb",
  "status": "Hard",
  "ipa": "/əˈbændən/",
  "definition": "To leave someone or something permanently.",
  "situation": "Ahmed stood at the door of his old apartment, took one last look, and walked away, abandoning everything he had built there.",
  "example": "I had to abandon my old phone because it kept freezing.",
  "image_prompt": "the word is Abandon, square image, 1:1 aspect ratio. An Egyptian man standing in the doorway of an old, sunlit apartment in Cairo, looking back one last time with a heavy but resolved expression, boxes half-packed behind him, dust in the afternoon light. write the word Abandon in English text centered at the top middle of the image",
  "notes": {
    "colloquial": "أسيبه، أرميه",
    "when_used": "لما حد يسيب شغله أو يسيب صاحبه ويمشي",
    "common_examples": "She decided to abandon her plans for the weekend.\nThe soldier had to abandon his post during the battle.",
    "sentence_structure": "abandon + something/someone",
    "synonyms": "leave, desert, forsake, give up",
    "antonyms": "keep, maintain, retain, hold on to",
    "common_mistakes": "بتتقال غالبًا مع حاجة ملموسة أو موقف، مش مع حاجات معنوية زي hope في الكلام اليومي",
    "important_notes": "كلمة قوية عاطفيًا — معناها إنك بتسيب حاجة بالكامل وخلاص، مش مجرد تأجيل"
  },
  "vault_root": "English"
}
```

`vault_root` is optional — it defaults to `"English"`. Pass a different value if the user's vault uses another top-level folder name.

The script will:
- Generate the image via a free, keyless image API and save it to `{vault_root}/Images/{Word}.jpeg`
- Generate pronunciation audio (word said 5 times) via `edge-tts` and save it to `{vault_root}/Listening/Pronunciation/{Word}_pronunciation.mp3`
- Generate example audio (example said 5 times) via `edge-tts` and save it to `{vault_root}/Listening/Examples/{word}_example.mp3`
- Write the full Obsidian note to `{vault_root}/Words/{Word}.md` using the template in `references/note_template.md`
- Write the Anki flashcard file to `{vault_root}/Flashcards/{Word}.txt`
- Copy the three media files into the AnkiDroid `collection.media` folder (copy, never move — the vault keeps its own copies)

The script already retries and falls back across models internally (see below), so a single call is normally enough — but still check its printed output for a final error before telling the user it's done.

If you're rebuilding a word the user already approved rebuilding in Step 0, add `--force` to the command.

## Notes on the pieces

- **Image generation**: uses `https://image.pollinations.ai` — no signup, no API key, just an HTTP GET with the prompt URL-encoded. This is what makes full automation possible without asking the user for credentials. The script tries a few different models in sequence (`flux` → `turbo` → `flux-realism`) and retries each a couple of times, so a single busy/broken response doesn't fail the whole build — you don't need to handle this manually.
- **Audio**: uses the `edge-tts` CLI (`en-US-BrianNeural`, natural speed), which the user already has installed locally.
- **Duplicate protection**: the script itself also refuses to overwrite an existing note unless `--force` is passed, as a safety net in case Step 0's check gets skipped somehow.
- **Anki media path**: defaults to `/home/nagdista/.local/share/Anki2/User 1/collection.media` — if a build fails because this path doesn't exist on the machine you're running on, ask the user for their actual AnkiDroid/Anki Desktop media folder and pass it with `--anki-media-dir`.

See `references/note_template.md` for the exact Obsidian note structure, and `references/example_abandon.md` for a complete worked example (word: "Abandon") showing every field filled in correctly.
