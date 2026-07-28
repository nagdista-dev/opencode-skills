---
name: vocab-maker
description: Build complete English vocabulary learning cards — an Obsidian note (definition, situation, example, IPA, Egyptian-dialect notes), an AI-generated illustrative image, and pronunciation + example audio via edge-tts — for one word or a batch of words, all saved inside the user's English folder. Use this skill whenever the user gives one or more English words and wants them "made" or "added" — e.g. "اعمل كلمة abandon", "make english word procrastinate", "ضيفلي vocab card لكلمة X", "اعمل الكلمات دي: abandon, procrastinate, resilient", or any request to turn English words/phrases/idioms into full study cards with image + audio.
---

# Vocab Maker

This skill turns one or more English words (or phrases/idioms) into complete, ready-to-study packages: an Obsidian note, an image that *is* the example sentence, and two audio files per word — with zero manual steps from the user afterward.

The mechanical work (calling the image API, calling edge-tts, writing files) is handled by `scripts/build_word.py`. Your job is the part that needs judgment: writing the content that goes into that script.

> **LEMMATIZATION — NON-NEGOTIABLE FIRST STEP.**
> Before doing anything else with a word, reduce it to its **base/root form (lemma)**:
> - Strip plural endings: `dogs` → `dog`, `abilities` → `ability`
> - Strip verb conjugations: `running` → `run`, `abandoned` → `abandon`, `goes` → `go`
> - Strip comparative/superlative forms: `faster` → `fast`, `biggest` → `big`
> - Strip adverb suffixes where the adjective is the base: `quickly` → `quick`
>
> The entire card — the note filename, the `word` field, the IPA, the image, and both audio files — is always built around the **lemma**, never the inflected form the user typed. This is critical: the student must memorize and recognize the root form of every word.

## Step 0 — Discover the English folder path

**This is the very first thing you do — before writing any content, before checking anything.** Ask the user:

> "عايزك تقولي مكان الـ English folder بتاعتك.
> - لو الفولدر موجود، ابعتلي الـ path كامل (مثال: `/home/user/Documents/english`)
> - لو مش موجود وعايز تعمله جديد، ابعتلي الـ path اللي عايز الفولدر يتعمل فيه وأنا هعمله ليك."

Wait for the user's reply. Do **not** proceed with any other step until you have a confirmed path.

Once you receive the path:

1. Resolve it to an absolute path (expand `~` if present).
2. **Read what is actually on disk** before deciding anything:
   ```bash
   ls -la "{english_folder}/"
   ```
   This is mandatory. You must see the real folder names that already exist — do not assume or invent names.
3. Map what you find to the four required roles:

   | Role | Look for a folder named (case-insensitive) |
   |---|---|
   | vocabulary | `vocabulary`, `words`, `vocab` |
   | images | `images`, `image`, `imgs` |
   | listening | `listening`, `audio`, `listen` |
   | pronunciation (inside listening) | `pronunciation`, `pronounce`, `pronun` |
   | examples (inside listening) | `examples`, `example`, `ex` |

   Use the **exact name that already exists on disk** for each role. If a folder for a role does not exist yet, create it using the preferred name from the table above (`vocabulary`, `images`, `listening/pronunciation`, `listening/examples`).

4. Create only the missing directories:
   ```bash
   mkdir -p "{path_to_missing_folder}"
   ```
5. Confirm the paths to the user and proceed immediately — do **not** wait for a reply:
   "تمام! هشتغل على الفولدرات دي:
   - كلمات: `{actual_vocabulary_path}`
   - صور: `{actual_images_path}`
   - نطق الكلمة: `{actual_pronunciation_path}`
   - نطق المثال: `{actual_examples_path}`"

Set these four resolved paths as your working variables for all subsequent steps — never hardcode or guess a path again.

---

## Step 1 — Check if this word already exists

Before writing anything, check whether the word already has a note:

```bash
ls "{actual_vocabulary_path}/{Word}.md" 2>/dev/null
```

(`{Word}` = first letter capitalized, e.g. `Abandon`. Use the resolved `{actual_vocabulary_path}` from Step 0, not a hardcoded path.)

- **If it exists**: tell the user the word already has a card, show them the existing note's Definition/Example so they can see what's there, and ask whether they want to rebuild it (pass `--force`) or leave it as is. Don't regenerate the image/audio unless they confirm.
- **If it doesn't exist**: proceed to Step 2 normally.

## Step 2 — Write the content

For the given word, produce these fields yourself. Take your time here — this is the part a script can't do, and the quality of the whole card depends on it.

| Field | What it is | Rules |
|---|---|---|
| `char` | First letter of the **lemma** | Uppercase |
| `type` | Noun / Verb / Phrase / Idiom / Adjective / ... | Pick the one that fits how the word is being taught |
| `status` | Difficulty tag | Default to `Hard` unless the user says otherwise |
| `ipa` | IPA transcription of the **lemma only** | Never the conjugated/inflected form — e.g. `/əˈbændən/` not `/əˈbændənd/` |
| `definition` | Plain English definition | One sentence, simple |
| `situation` | A short narrative scene in English showing the word's meaning through context | Third person, a little story — this is what the image will be built from |
| `example` | A short, memorable example sentence in English | **CRITICAL**: The example must be very short, simple, and highly expressive. It must **always** be in the first person ("I", "my" - على لساني) so the user can easily remember and memorize it. **The image and the example must have a direct, 1:1 correlation (علاقة طردية). The image must perfectly express the exact situation in the example.** |
| `notes` | Detailed notes in Egyptian Arabic dialect | See sub-fields below — write each field as flowing prose, no tables, no emojis |

`notes` sub-fields (all in Egyptian Arabic, casual and practical — this is the part that makes the word actually stick for an Egyptian learner):
- `colloquial` — إيه أقرب معنى بالعامي المصري
- `when_used` — امتى الكلمة دي بتتقال في كلام عادي
- `common_examples` — 2-3 جمل تانية غير المثال الأساسي (مع ترجمة لو محتاجة)
- `synonyms` — مرادفات إنجليزي
- `antonyms` — أضداد إنجليزي
- `common_mistakes` — الأخطاء الشائعة اللي المصريين بيقعوا فيها مع الكلمة دي
- `important_notes` — أي حاجة تانية مهمة (نبرة الكلمة، سياقها العاطفي، إلخ)

> **NO EMOJIS OR ICONS — EVER.** The notes section (and the entire note file) must contain plain text only. No emoji characters, no icon characters, no decorative symbols of any kind — not in headings, not in content, not anywhere. This is a hard rule with no exceptions.

**Note rendering format for specific sections (applied automatically by the script):**
- `common_examples` — each example line is wrapped in its own ` ```text ``` ` code block
- `synonyms` — wrapped in a single ` ```text ``` ` code block
- `antonyms` — wrapped in a single ` ```text ``` ` code block
- All other notes fields are rendered as plain text


## Step 3 — Build the image prompt

Write one `image_prompt` string. It **must** follow this exact shape:

1. Start with: `the word is {Word}, square image, 1:1 aspect ratio.`
2. Then a detailed visual description of the **example sentence** as a real scene — people, expressions, atmosphere, colors, location, small details. **Set it in everyday Egyptian life** (a Cairo street, a Metro carriage, a baladi apartment, a coffeeshop, a microbus, a university lecture hall, etc.) so the imagery feels familiar and personal rather than generic stock-photo Western imagery.
3. End with: `write the word {Word} in English text centered at the top middle of the image`

The prompt is not just a caption — it *is* a visual realization of the example. There must be a direct correlation (علاقة طردية) between the example you wrote and the image you generate. They must match perfectly. See `references/example_abandon.md` for a full worked example of this end-to-end.

## Step 4 — Run the build script

Once you have written all the content, call the build script immediately — do **not** show a preview, do **not** ask for approval first. Just run it.

**If the user sent more than one word**, process them all **sequentially without stopping**. Complete each word fully (Steps 2–4) before moving to the next. Do not ask for permission between words, do not pause to confirm, do not summarize between words — just keep going until every word in the list is done, then report the final results all at once.


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
  "vocabulary_path": "{actual_vocabulary_path}",
  "images_path": "{actual_images_path}",
  "pronunciation_path": "{actual_pronunciation_path}",
  "examples_path": "{actual_examples_path}"
}
```

Replace the four `{actual_*_path}` placeholders in the JSON with the real resolved paths from Step 0. These are **required** — never leave them as template strings, never assume a default.

The script will:
- Generate the image and save it to `{actual_images_path}/{Word}.jpeg`
- Generate pronunciation audio (word, 5 times, 0.5 s gap) and save it to `{actual_pronunciation_path}/{Word}_pronunciation.mp3`
- Generate example audio (example, 5 times, 0.5 s gap) and save it to `{actual_examples_path}/{word}_example.mp3`
- Write the full Obsidian note to `{actual_vocabulary_path}/{Word}.md` using the template in `references/note_template.md`

The script already retries and falls back across models internally (see below), so a single call is normally enough — but still check its printed output for a final error before telling the user it's done.

If you're rebuilding a word the user approved rebuilding in Step 1, add `--force` to the command.

## Notes on the pieces

### Image generation

Uses **Pollinations.ai** exclusively (free open-source image generation, no API key required):
- URL format: `https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true`
- Image is always saved as `{Word}.jpeg` at 1:1 aspect ratio

### Audio

Uses the `edge-tts` CLI with the voice `en-US-BrianNeural` — **MALE VOICE IS MANDATORY. Never use a female voice under any circumstance.** Brian is an American English male voice, clear and natural. Both the pronunciation file and the example file repeat their content **5 times** with a **0.5-second silence between each repetition**, paced like a teacher saying it slowly and clearly to a student learning for the first time. If `en-US-BrianNeural` is unavailable, fall back to another male US English voice (e.g. `en-US-GuyNeural`) — never a female one.

### Duplicate protection

The script refuses to overwrite an existing note unless `--force` is passed, as a safety net in case Step 1's check gets skipped somehow.

See `references/note_template.md` for the exact Obsidian note structure, and `references/example_abandon.md` for a complete worked example (word: "Abandon") showing every field filled in correctly.
