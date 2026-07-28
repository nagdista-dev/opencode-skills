# Worked Example: "Abandon"

This shows a complete, correctly-filled JSON input and the note it produces, end to end.

## Input JSON

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
  "image_prompt": "the word is Abandon, square image, 1:1 aspect ratio. An Egyptian man standing in the doorway of an old, sunlit apartment in Cairo, looking back one last time with a heavy but resolved expression, boxes half-packed behind him, dust visible in the afternoon light, warm ochre walls, a ceiling fan frozen mid-spin. write the word Abandon in English text centered at the top middle of the image",
  "notes": {
    "colloquial": "أسيبه، أرميه",
    "when_used": "لما حد يسيب شغله أو يسيب صاحبه ويمشي",
    "common_examples": "She decided to abandon her plans for the weekend.\nThe soldier had to abandon his post during the battle.",
    "sentence_structure": "abandon + something/someone",
    "synonyms": "leave, desert, forsake, give up",
    "antonyms": "keep, maintain, retain, hold on to",
    "common_mistakes": "بتتقال غالبًا مع حاجة ملموسة أو موقف، مش مع حاجات معنوية زي hope في الكلام اليومي",
    "important_notes": "كلمة قوية عاطفيًا — معناها إنك بتسيب حاجة بالكامل وخلاص، مش مجرد تأجيل"
  }
}
```

## Why this is a good example (not just a valid one)

- **`situation` and `example` describe the same moment** — a phone being abandoned — not two unrelated ideas. The image prompt is built from that one moment, in detail.
- **The scene is Egyptian and specific** (Cairo apartment, ochre walls, ceiling fan) rather than "a person leaving a house" — this is what makes the image memorable instead of generic.
- **The example is short and in first person** ("I had to...") — something the learner can imagine saying themselves, not a line from a story about someone else.
- **The Arabic notes add what the English definition can't** — when Egyptians actually say this word, and the mistake pattern specific to Arabic speakers (using it with abstract nouns the way "التخلي عن الأمل" would translate, which sounds off in everyday English).

## Resulting note (`English/Words/Abandon.md`)

```markdown
---
char: A
type: Verb
status: Hard
image: Abandon.jpeg
prompt: the word is Abandon, square image, 1:1 aspect ratio. An Egyptian man standing in the doorway of an old, sunlit apartment in Cairo, looking back one last time with a heavy but resolved expression, boxes half-packed behind him, dust visible in the afternoon light, warm ochre walls, a ceiling fan frozen mid-spin. write the word Abandon in English text centered at the top middle of the image
---

## Abandon Info

| Word       | Abandon                                                                     |
| ---------- | ---------------------------------------------------------------------------|
| Situation  | Ahmed stood at the door of his old apartment, took one last look, and walked away, abandoning everything he had built there |
| Definition | To leave someone or something permanently                                  |
| Example    | I had to abandon my old phone because it kept freezing.                    |
| IPA        | `/əˈbændən/`                                                                |

## Abandon Pronunciation

![[Abandon_pronunciation.mp3]]

## Abandon Example

![[abandon_example.mp3]]

## Abandon Notes

### بالعامية المصرية
أسيبه، أرميه

### إمتى بتتقال؟
لما حد يسيب شغله أو يسيب صاحبه ويمشي

### أمثلة شائعة

```text
She decided to abandon her plans for the weekend.
```

```text
The soldier had to abandon his post during the battle.
```

### مرادفات (Synonyms)

```text
leave, desert, forsake, give up
```

### أضداد (Antonyms)

```text
keep, maintain, retain, hold on to
```

### أخطاء شائعة
بتتقال غالبًا مع حاجة ملموسة أو موقف، مش مع حاجات معنوية زي hope في الكلام اليومي

### ملاحظات مهمة
كلمة قوية عاطفيًا — معناها إنك بتسيب حاجة بالكامل وخلاص، مش مجرد تأجيل

![[Abandon.jpeg]]
```
