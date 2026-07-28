# Obsidian Note Template

This is the exact structure `scripts/build_word.py` renders into `{vault_root}/Words/{Word}.md`.
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

| العنصر | التفاصيل |
|--------|----------|
| بالعامية | {notes.colloquial} |
| امتى بتتقال | {notes.when_used} |
| أمثلة شائعة | {notes.common_examples} |
| تركيب الجملة | {notes.sentence_structure} |
| مرادفات | {notes.synonyms} |
| antonyms | {notes.antonyms} |
| أخطاء شائعة | {notes.common_mistakes} |
| ملاحظات مهمة | {notes.important_notes} |

![[{Word}.jpeg]]
```

## AnkiDroid flashcard line

Written to `{vault_root}/Flashcards/{Word}.txt`, tab-separated, one line, HTML allowed on import:

```
<img src="{Word}.jpeg" width="200"><br>{Word}<br>[sound:{Word}_pronunciation.mp3]	{example} [sound:{word}_example.mp3]
```

Naming rules:
- `{Word}` = first letter capital, rest lowercase (e.g. `Abandon`)
- `{word}` = all lowercase (e.g. `abandon`) — used only for the example audio filename
