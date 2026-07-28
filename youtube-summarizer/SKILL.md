---
name: youtube-summarizer
description: >
  Summarizes a YouTube video into a beautifully structured Obsidian Markdown note.
  Automatically fetches the video transcript (no API key needed), analyzes the
  content, and produces a rich formatted note with key insights, structured sections,
  notable quotes, and actionable takeaways — saved directly into the user's vault.
  Trigger with any YouTube link plus a summary request, e.g. "لخصلي الفيديو ده",
  "summarize this youtube video", or "اعمل ملخص لـ <URL>".
context: fork
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
argument-hint: "<YouTube URL> [save path]"
---

# YouTube Summarizer

This skill converts any YouTube video into a complete, richly-formatted Obsidian note using only free tools. The Python script handles transcript fetching; you handle the intelligence: analyzing, structuring, and writing a summary that actually *sticks*.

---

## Step 0 — Discovery & Setup

Ask all questions in a **single message**. Do not ask them one by one.

```
أهلاً! هنعمل ملخص احترافي للفيديو ده في Obsidian. محتاج منك ٥ معلومات:

١. رابط الفيديو (YouTube URL)؟
٢. مسار الفولدر اللي هحفظ فيه الملف (مثال: /home/user/Obsidian/Vault/YouTube)؟
٣. عايز التلخيص بأي لغة؟
   [1] English
   [2] عربي فصيح
   [3] عربي مصري عامي
   [4] Bilingual — English headings + عربي مصري للشرح
٤. عايز أي نوع تلخيص؟
   [A] Quick Brief   — فكرة رئيسية + ٧ نقاط مهمة (سريع ومفيد)
   [B] Deep Dive     — تحليل عميق بأقسام وأمثلة واقتباسات
   [C] Study Notes   — نوتس دراسية بمصطلحات وأسئلة مراجعة
   [D] Action Plan   — خطة عمل عملية وخطوات قابلة للتنفيذ
٥. عايز الملخص يحتوي على إيموجي ولا تفضل الملف نظيف بدونها؟
   [Y] نعم — استخدم إيموجي في العناوين والنقاط
   [N] لا  — نص نظيف بدون إيموجي خالص
```

**MANDATORY**: Do not proceed until the user has answered all five questions. Store the emoji preference as `use_emoji` (true/false) and apply it consistently across the entire generated note and all confirmation messages.

---

## Step 1 — Fetch the Transcript

Run the transcript script with the provided URL:

```bash
python3 "$(dirname "$0")/scripts/fetch_transcript.py" --url "$ARGUMENTS"
```

Or if the URL was provided interactively:

```bash
python3 scripts/fetch_transcript.py --url "<USER_PROVIDED_URL>"
```

The script outputs a JSON object to stdout:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title Here",
  "channel": "Channel Name",
  "duration": "3:32",
  "transcript": "Full transcript text here...",
  "language": "en",
  "status": "ok"
}
```

**Parse the JSON output and extract all fields.** If `status` is not `"ok"`, tell the user what went wrong (e.g., no captions, private video) and stop.

---

## Step 2 — Internal Content Analysis

Before writing a single word, perform this internal analysis (do not show to user unless asked):

- **Core Thesis**: What is the single most important argument or idea?
- **Key Concepts**: List the 3–7 main concepts or arguments.
- **Notable Quotes**: Identify 1–3 memorable, quotable sentences.
- **Structure**: What narrative pattern does the video follow? (problem→solution, list, story→lesson, interview, tutorial, etc.)
- **Tone**: Educational / Motivational / Technical / Journalistic / Entertainment?
- **Target Audience**: Beginners / Experts / General public?
- **Topic Tags**: 2–4 relevant Obsidian tags (e.g., `productivity`, `psychology`, `programming`).

Use this analysis to shape the summary for the chosen language and style.

---

## Step 3 — Preview & Approval

**Do not write the file yet.** Show a quick preview in chat:

```
✅ تم جلب الترانسكريبت بنجاح!

📺 الفيديو: <title>
📡 القناة: <channel>
⏱️ المدة: <duration>

📝 الأوتلاين المقترح للتلخيص:
<outline of planned sections based on chosen style>

الأوتلاين ده مناسب؟ ولا في حاجة عايزها تختلف قبل ما أكتب التلخيص الكامل؟
```

- **Approved** → proceed to Step 4.
- **Changes requested** → revise the plan and confirm again. Never write the file without explicit approval.

---

## Step 4 — Write the Obsidian Note

### Filename Convention

Generate the filename from the video title:
- Lowercase everything
- Replace spaces with hyphens
- Remove all characters except letters, numbers, and hyphens
- Max 60 characters
- Append `.md`

Example: `"How to Build Atomic Habits (Full Guide)"` → `how-to-build-atomic-habits-full-guide.md`

### YAML Frontmatter

Every note must begin with this complete frontmatter block:

```yaml
---
title: "<Video Title>"
source: "<YouTube URL>"
channel: "<Channel Name>"
duration: "<MM:SS or HH:MM:SS>"
date_summarized: "<YYYY-MM-DD>"
summary_language: "<English | عربي فصيح | عربي مصري | Bilingual>"
summary_style: "<Quick Brief | Deep Dive | Study Notes | Action Plan>"
tags:
  - youtube-summary
  - <topic_tag>
  - <topic_tag>
status: summarized
---
```

### Universal Formatting Rules

Apply these rules across **all styles and all languages**:

| Element | Obsidian Syntax | When to Use |
|---------|-----------------|-------------|
| Document title | `# H1` — one per note | Video title |
| Major sections | `## H2` | Top-level sections |
| Sub-sections | `### H3` | Details within a section |
| Section breaks | `---` | Between every major section |
| Key terms | `**bold**` | First mention of important concepts |
| Critical insight | `==highlighted==` | The single most important sentence per section |
| Speaker quotes | `> blockquote` | Direct quotations |
| Action items | `- [ ] checkbox` | Anything the user can act on |
| Internal links | `[[wikilink]]` | Concepts that may link to other vault notes |

**Callout blocks** — use Obsidian's native callout syntax:

```markdown
> [!IMPORTANT]
> The core thesis or single most critical insight.

> [!NOTE]
> Background context or definition of a technical term.

> [!TIP]
> A practical tip directly from the video.

> [!WARNING]
> A cautionary point or common mistake the speaker warns against.

> [!QUOTE]
> A notable direct quote from the speaker.
```

---

### Style A — Quick Brief (موجز سريع)

Best for: fast consumption, skimming before watching.

```markdown
# <Video Title>

> [!IMPORTANT]
> **الفكرة الجوهرية**: <One sentence — the single core takeaway from this video.>

---

## Overview
<2–3 sentences. What is this video about? Why does it matter?>

---

## Key Takeaways
- **<Point 1>**: <explanation>
- **<Point 2>**: <explanation>
- **<Point 3>**: <explanation>
- **<Point 4>**: <explanation>
- **<Point 5>**: <explanation>

---

## Bottom Line
==<The single most important sentence to remember from this entire video.>==

---

## Source

- [Watch Video](<URL>) — <Channel Name> — <Duration> — Summarized: <Date>
```

> **Emoji rule**: If `use_emoji` is true, prefix each Source item with a relevant emoji. If false, omit all emoji from the entire note.

---

### Style B — Deep Dive (تحليل عميق)

Best for: comprehensive understanding, reference notes.

```markdown
# <Video Title>

> [!IMPORTANT]
> **Core Thesis**: <The central argument or claim the video makes.>

---

## Overview
<3–4 paragraphs. What is this video about? Who made it and why? What question does it set out to answer? Why should the reader care?>

---

## Main Ideas

### 1. <Idea Name>
<Explanation of the idea with context from the video...>

> [!QUOTE]
> "<Direct quote from the speaker>"

### 2. <Idea Name>
<Explanation...>

> [!TIP]
> <Practical implication of this idea.>

### 3. <Idea Name>
<Explanation...>

---

## Key Concepts & Definitions

| Concept | Definition |
|---------|-----------|
| [[<Term 1>]] | <Clear, simple definition> |
| [[<Term 2>]] | <Clear, simple definition> |

---

## Notable Quotes

> [!QUOTE]
> "<Most impactful quote>"
> — <Speaker Name>

> [!QUOTE]
> "<Second quote if available>"

---

## My Notes & Reflections
> **أفكاري أنا:**
> *(اكتب هنا أفكارك وردود فعلك بعد ما تتفرج على الفيديو)*

---

## Action Plan
- [ ] <Concrete action step 1>
- [ ] <Concrete action step 2>
- [ ] <Concrete action step 3>

---

## Source

- [Watch Video](<URL>) — <Channel Name> — <Duration> — Summarized: <Date>
```

---

### Style C — Study Notes (نوتس دراسية)

Best for: academic content, courses, technical lectures.

```markdown
# <Video Title>

---

## The Big Picture
<What is this about? Why should I study this? What will I know by the end?>

---

## Lecture Outline
1. <Topic A>
2. <Topic B>
3. <Topic C>

---

## Detailed Notes

### 1. <Topic A>
<Detailed notes in the chosen language...>

> [!NOTE]
> **Definition — <Term>**: <Simple, clear definition.>

==<Most important sentence from this section.>==

### 2. <Topic B>
<Notes...>

### 3. <Topic C>
<Notes...>

---

## Glossary

| Term | Meaning |
|------|---------|
| [[<Term 1>]] | <Definition> |
| [[<Term 2>]] | <Definition> |

---

## Self-Test Questions

1. <Question about Topic A>?
2. <Question about Topic B>?
3. <Question about Topic C>?

---

## Answers

> [!NOTE] Answers — reveal only after attempting
> **1.** <Answer to Q1>
>
> **2.** <Answer to Q2>
>
> **3.** <Answer to Q3>

---

## Source

- [Watch Video](<URL>) — <Channel Name> — <Duration> — Summarized: <Date>
```

---

### Style D — Action Plan (خطة عمل)

Best for: self-improvement, how-to, business, productivity videos.

```markdown
# <Video Title>

> [!IMPORTANT]
> **المشكلة اللي الفيديو بيحلها**: <One sentence.>

---

## What This Video Is About
<2 sentences. What problem or goal does this video address?>

---

## The Core Method / Framework
<Explain the main system, method, or approach taught in the video.>

---

## Step-by-Step Action Plan

### Phase 1: <Phase Name>
- [ ] <Specific action — be precise, not vague>
- [ ] <Specific action>

### Phase 2: <Phase Name>
- [ ] <Specific action>
- [ ] <Specific action>

### Phase 3: <Phase Name> *(if applicable)*
- [ ] <Specific action>

---

## Common Mistakes to Avoid

> [!WARNING]
> <Most critical mistake the speaker warns against, and why.>

- ❌ <Mistake 1> → ✅ <What to do instead>
- ❌ <Mistake 2> → ✅ <What to do instead>

---

## Resources Mentioned
- <Resource 1 name and link if available>
- <Resource 2 name and link if available>

---

## Source

- [Watch Video](<URL>) — <Channel Name> — <Duration> — Summarized: <Date>
```

---

## Step 5 — Save the Note

Write the note to the user's specified save location:

```bash
mkdir -p "<save_location>"
cat > "<save_location>/<filename>.md" << 'OBSIDIAN_NOTE'
<full note content>
OBSIDIAN_NOTE
```

Confirm success to the user with a plain-text message (emoji only if `use_emoji` is true):

```
تم الحفظ!

الملف: <filename>.md
المسار: <full path>
الملخص: <one-line description of what the note contains>

تقدر تفتح الملف في Obsidian وتضيف ملاحظاتك الشخصية في قسم "My Notes".
```

---

## Tooling Notes

- **Transcript library**: `youtube-transcript-api` (pip install, free, no API key, no signup).
- **Supported content**: Public videos with manual or auto-generated subtitles. Does **not** work on private, age-restricted, or DRM-protected videos.
- **Language handling**: The script tries to fetch in the video's primary language. If the video has multiple subtitle tracks, it picks the one closest to the user's chosen summary language.
- **Caching**: Transcripts are cached at `scripts/.cache/transcript_<video_id>.txt`. Delete to force a fresh fetch.
- **Filename safety**: Titles are sanitized to lowercase hyphenated slugs, max 60 chars, alphanumeric + hyphens only.

See `references/note_template.md` for the blank template and `references/example_note.md` for a complete worked example.
