# Obsidian Note Template

This is the exact structure `scripts/build_word.py` renders into `{english_folder}/vocabulary/{Word}.md`.
You don't need to write this file yourself — the script fills it in from your JSON — but understanding
the shape helps you write better `situation`/`example`/`notes` content.

```markdown
---
char: {char}
type: {type}
status: {status}
image: {Word}.jpeg
prompt: {image_prompt}
---

## {Word} Info

| Word       | {Word}       |
| ---------- | ------------ |
| Situation  | {situation}  |
| Definition | {definition} |
| Example    | {example}    |
| IPA        | `{ipa}`      |

## {Word} Pronunciation

![[{Word}_pronunciation.mp3]]

## {Word} Example

![[{word}_example.mp3]]

## {Word} Notes

### بالعامية المصرية
{notes.colloquial}

### إمتى بتتقال؟
{notes.when_used}

### أمثلة شائعة

```text
{notes.common_examples (each line in its own code block)}
```

### مرادفات (Synonyms)

```text
{notes.synonyms}
```

### أضداد (Antonyms)

```text
{notes.antonyms}
```

### أخطاء شائعة
{notes.common_mistakes}

### ملاحظات مهمة
{notes.important_notes}

![[{Word}.jpeg]]
```

Naming rules:
- `{Word}` = first letter capital, rest lowercase (e.g. `Abandon`)
- `{word}` = all lowercase (e.g. `abandon`) — used only for the example audio filename
