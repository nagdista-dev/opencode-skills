---
name: convert-to-mind-map
version: "1.0"
description: Use this skill whenever the user wants to convert one or more Markdown files into an Obsidian Markmind mind map (e.g. "حوّل الملف ده لـ mind map", "عايز أعمل mind map من الـ notes دي", "Convert this to a mind map", "اعمللي mind map من الفولدر ده"). This skill reads existing Markdown files from a user-specified folder, intelligently analyzes their content and structure, and produces ready-to-open Markmind-compatible `.md` files (using `mindmap-plugin: basic` frontmatter) inside the same vault. ALWAYS use this skill (not a generic explanation) whenever the user asks to convert notes, files, or a folder into a mind map, visual map, or Markmind board — even if they don't say the word "skill" explicitly.
---

# Convert to Mind Map — Obsidian Markmind Skill

## What This Skill Does

This skill reads one or more existing Markdown notes from a folder the user points to, then produces a well-structured Markmind-compatible mind map file (`.md`) that Obsidian can open directly as a visual mind map using the **Markmind plugin** (Basic mode). The AI does the heavy lifting: it reads, understands, groups, and restructures the content into a clean hierarchy — the user gets a ready-to-open mind map with zero manual work.

---

## Markmind Plugin — Quick Reference

This skill uses the **Obsidian Markmind plugin** (Basic mode only) to produce mind maps.

**Key facts to keep in mind:**
- Output files must start with `mindmap-plugin: basic` in their YAML frontmatter — without it, Obsidian won't open the file as a mind map.
- Structure = one `# H1` root + `##`/`###` headings as branches + `- bullets` as child nodes.
- Inline Markdown renders inside nodes: bold, italic, inline code, wikilinks, emojis, KaTeX math.
- Tables, callouts, and code fences do NOT render as nodes — never put them in the map body.
- Checkboxes (`- [ ]`) render as toggleable task nodes.
- Export available via `Ctrl+P`: "Export to HTML" or "Export mindmap as a PDF file".
- Embedding in other notes: `![[mind-map-filename]]`.

> For full syntax details, mode options, and feature reference, read `references/markmind-plugin.md`.

---

## Language & Register

- Talk in **حقيقي عامية مصرية شارع** — كلام طبيعي، مش فصحى. يعني "هنعمل"، "بص"، "خلاص"، "كده"، "عادي" — كلها طبيعية.
- الـ technical terms بتفضل إنجليزي دايماً: `mind map`, `node`, `branch`, `frontmatter`, `wikilink`, `heading`, `Markmind`. **متترجمهاش أبداً.**
- لو الجملة ممكن تتقال في نشرة أخبار، ده معناه إنها formal أوي — أعد صياغتها.
- **RTL flow rule:** أي سطر أو heading بيبدأ بكلمة إنجليزية، حط قدامها "الـ" عشان السطر يبدأ بعربي. مثال: "الـ Markmind بيشتغل..." مش "Markmind بيشتغل...".
- **Filenames are always English kebab-case** — no Arabic in filenames ever.

---

## Language of Nodes

The language the AI uses for the **node text inside the mind map file** is controlled entirely by the user's answer in Step 0. This is separate from the conversational language above (which is always Egyptian Arabic).

| User chose | How to write node text |
|---|---|
| **Arabic** | Write node explanations and descriptions in Arabic. **Technical terms — any named concept, tool, function, framework, protocol, or technology that has an established English name — ALWAYS stay in English, no exceptions.** Never invent an Arabic equivalent for a technical term. |
| **English** | Write all node labels in English. Keep them concise and clear. |

**Arabic mode — absolute rule, cannot be overridden:** "Arabic" means the *explanatory words* are Arabic — it does NOT mean translating technical terms. The user chose Arabic so they can read the context and descriptions in their language; they did NOT ask you to invent Arabic names for things that don't have Arabic names.

- ✅ CORRECT: `- بتخزّن الـ **state** جوه الـ component`
- ✅ CORRECT: `- الـ API بترجع JSON`
- ✅ CORRECT: `## ⚙️ الـ useEffect`
- ❌ WRONG: `- بتخزّن الـ **حالة** جوه الـ مكوّن` — (translated `state` → حالة and `component` → مكوّن)
- ❌ WRONG: `## الخطاف` — (translated `hook`)
- ❌ WRONG: `- الـ واجهة البرمجية ترجع بيانات` — (translated `API` and `JSON`)

This rule is identical to the `study-programming` skill and applies everywhere in the output file: headings, bullet nodes, root node — everywhere.

**The example output in the Reference section at the bottom of this file is in Arabic mode.** If the user picks English, write equivalent English labels instead.

---

## Workflow

### Step 0 — Get the source location (FIRST thing you do, always)

**The very first action of this skill — before any analysis, before any file creation, before anything else — is to ask the user where the source is.** Never skip this step or assume a location.

1. **Ask first:** "فين الفولدر أو الملف اللي عايز تعمل منه الـ mind map؟" — wait for the user to provide an exact path before proceeding.
2. Ask: "عايز mind map واحد للكل، ولا mind map لكل ملف لوحده؟" — clarify the aggregation strategy:
   - **One map per file** — each `.md` source gets its own Markmind output file saved next to it.
   - **One combined map** — all files are analyzed together and merged into a single hierarchical mind map.
3. Ask: "عايز الـ mind map يكون بالعربي ولا بالإنجليزي؟" — the user's answer governs the language of all node text in the output (see Language of Nodes section below).

**Output location rule (no need to ask — it's automatic):**
- If the user gave a **folder path**: the output `.md` file(s) are saved **inside that same folder**.
- If the user gave a **single file path**: the output `.md` is saved **in the same directory as that file** (i.e., right next to it).

**Never create any file until you have the source path, aggregation preference, and language preference confirmed.** If any answer is vague or ambiguous, ask a short follow-up to get the exact answer.

#### Customization Preferences (ask after the 3 questions above)

Once source, aggregation, and language are confirmed, ask the user about their visual preferences **before** reading any file. Present these as a friendly single message — not a formal form. Example opener: "كويس! قبل ما أبدأ، عايزني أعرف تفضيلاتك عشان الـ mind map تطلع على حسب اللي بتحبه — ردّ على الأسئلة دي بسرعة:"

Ask about each of the following in one message:

**1. الـ Emojis**
- "تحب أحط emoji في أول كل branch، ولا تفضل نص بدون emojis؟"
- Options: **آه** (on) / **لا** (off) / **أنت شوف** (AI decides per content)
- Default if skipped: on

**2. الـ Content Density**
- "الـ mind map تكون شاملة (كل المعلومات) ولا مركّزة (أهم النقاط بس)؟"
- Options:
  - **شاملة** — every section, point, and sub-item. Best for study/reference.
  - **مركّزة** — main ideas only. Best for overview/quick review.
- Default if skipped: شاملة (comprehensive)

**3. الـ Depth**
- "عايز الـ map تتفرع لأد إيه؟"
- Options: **سطحية** (2 levels: root + branches) / **متوسطة** (3 levels) / **عميقة** (4 levels)
- Default if skipped: متوسطة (3 levels)

**4. الـ Checkboxes**
- "لو لقيت خطوات أو مهام، أحولها لـ checkboxes؟"
- Options: **آه** / **لا**
- Default if skipped: آه (yes)

**5. ملاحظة مهمة عن الألوان — قولها للمستخدم:**

> "بخصوص الألوان: الـ Markmind Basic mode مش بيدعم تلوين الـ nodes من خلال الـ Markdown — ده بيحتاج الـ Rich mode اللي بيخزن JSON وصعب تعدله يدوياً. بنستخدم الـ Basic mode عشان يكون الملف قابل للقراءة والتعديل بسهولة. بدل الألوان، بنستخدم الـ emojis كـ visual markers + **bold** للمصطلحات المهمة + `inline code` للأسماء التقنية — وده بيدي شكل احترافي ومنظم. لو عايز ألوان فعلية، هتحتاج تضيفها يدوياً من داخل الـ Markmind app بعد ما تفتح الـ mind map."

**Preferences profile:** Collect all 4 answers and apply them consistently across every output file in this session. If the user skips an answer, apply the stated default silently without asking again.

**Interactivity rule for Step 0:** After collecting all preferences, confirm the full profile in one message before starting — e.g. "تمام! الملخص: فولدر X — mind map واحدة — عربي — مع emojis — شاملة — 3 مستويات — مع checkboxes. هبدأ أقرأ الملفات؟" — wait for confirmation.

---

### Step 1 — Read and analyze the source files

For each source Markdown file:
1. Read the full content.
2. Identify the main topic/title (from the `# H1`, the `title:` frontmatter field, or the filename — in that order of priority).
3. **Infer the naming convention** from the existing filenames in the source folder — look at how the other `.md` files are named and detect the pattern:

   | Pattern example | Convention |
   |---|---|
   | `react-hooks-notes.md` | kebab-case |
   | `ReactHooksNotes.md` | PascalCase |
   | `react_hooks_notes.md` | snake\_case |
   | `React Hooks Notes.md` | Title Case with spaces |
   | `2026-07-27-react-hooks.md` | date-prefix + kebab-case |
   | `27-07-2026 React Hooks.md` | date-prefix + Title Case |
   | `01 - React Hooks.md` | number-prefix + Title Case |

   If the folder has mixed conventions, pick the most common one. If only one file is given (no folder context), infer from that file's own name.

4. Extract the key concepts, sections, and sub-points. Strip out prose filler — you're extracting *structure and key ideas*, not copying paragraphs.
5. Note any existing headings (`##`, `###`) — these become natural branches.
6. Note any existing lists — these become child nodes.
7. Note any wikilinks `[[...]]` inside the source — preserve them as-is in the mind map nodes; they stay clickable in Obsidian.
8. Note the source file's frontmatter properties (tags, aliases, dates) — you may use tags as branch labels if relevant.

**Key analysis question to answer per file:** "لو هتشرح الملف ده لحد في 10 كلمات أو أقل لكل فكرة، إيه أهم الأفكار اللي فيه وعلاقتها ببعض؟"

---

### Step 2 — Design the mind map structure

Before writing any file, plan the hierarchy:

- **Root node** = the main topic of the file (or the overall collection topic if combining multiple files).
- **First-level branches (`##`)** = major sections or themes.
- **Second-level branches (`###`)** = sub-sections under each major theme.
- **Bullet nodes (`-`)** = specific points, facts, steps, or items.

**Completeness rule (critical):** The mind map must represent **all meaningful information** from the source file(s) — not just highlights or a summary. Every section, every key point, every step, every named concept must appear as a node. The only things you may omit are: filler prose ("in this section we will..."), pure formatting artifacts, and duplicate repetitions of the same idea. If the source is detailed, the mind map is detailed too.

**Structure rules:**
- Keep node text **concise** — max 10 words per node. Compress prose into a tight label, but include the full idea.
- Aim for **balance** — branches shouldn't be wildly unequal (one branch with 20 nodes, another with 1). Regroup if needed.
- **Max depth of 4 levels** in Basic mode for readability (Root → `##` → `###` → `-` → `  -`). Don't nest deeper.
- If combining multiple files: each source file becomes a `##` branch, with its full internal structure underneath.

**Interactivity rule for Step 2:** For large or complex sources, briefly tell the user what structure you're planning before writing the file — e.g. "لقيت 5 أقسام رئيسية في الملف، هعملهم 5 branches. هبدأ أكتب الـ mind map؟" — and proceed after confirmation.

---

### Step 3 — Create the output mind map file(s)

For each output file:

1. **Filename — infer, don't default:** Do not blindly use kebab-case. Instead, apply the naming convention you detected in Step 1 from the source folder's existing files. Append a suffix that matches the same style:

   | Detected convention | Output filename example |
   |---|---|
   | `react-hooks-notes.md` (kebab-case) | `react-hooks-mindmap.md` |
   | `ReactHooksNotes.md` (PascalCase) | `ReactHooksMindmap.md` |
   | `react_hooks_notes.md` (snake\_case) | `react_hooks_mindmap.md` |
   | `React Hooks Notes.md` (Title Case) | `React Hooks Mindmap.md` |
   | `2026-07-27-react-hooks.md` (date + kebab) | `2026-07-27-react-hooks-mindmap.md` |
   | `01 - React Hooks.md` (number + Title) | `01 - React Hooks Mindmap.md` |

   The mind map filename = source slug (in the same style) + the word `mindmap` (or `Mindmap` / `MindMap` / `mind-map` / `mind_map` matching the convention). If combining multiple files into one map, derive a descriptive combined name following the same convention. The file is always saved in the **same folder** as the source file(s).

2. **Frontmatter:** Always include:
```yaml
---
mindmap-plugin: basic
tags: [mind-map, <topic-tag>]
source: "[[<original-filename>]]"
created: <YYYY-MM-DD>
---
```

3. **Structure:** Follow the Basic mode format exactly — one `# Root`, then `##`/`###` headings, then `- bullet` lists.

4. **Visual styling (mandatory — not optional):** Markmind Basic mode renders standard Markdown formatting inside nodes. Use these consistently to make the map look professional and visually organized:

   **Emoji category icons on `##` branch headings** — pick one emoji per branch that semantically matches the topic and put it at the start of the heading. Use a consistent system, for example:
   - 🎯 for goals / objectives
   - 📋 for steps / processes / how-to
   - ⚙️ for technical details / configuration
   - 💡 for concepts / theory / ideas
   - ⚠️ for warnings / caveats / important notes
   - ✅ for results / outcomes / conclusions
   - 🔗 for links / references / resources
   - 📊 for data / metrics / numbers
   - 🏗️ for architecture / structure / design
   - 🛠️ for tools / setup / installation
   
   Choose the emoji that best fits each branch — don't force a category that doesn't fit, and don't use the same emoji for every branch.

   **Bold for key terms inside nodes:** wrap the single most important word or term in a node with `**bold**`. Don't over-bold — one bold element per node max.

   **Inline code for technical identifiers:** any function name, command, file path, variable, or code element inside a node gets wrapped in backticks: `` `useState` ``, `` `npm install` ``, `` `.env` ``.

   **Checkboxes for actionable items:** if a node represents a task, step, or something the user must do, use `- [ ]` instead of `-`.

5. **Wikilinks:** Preserve any `[[...]]` from the source file as-is. Add new wikilinks if a node references another note the user likely has.

6. **No prose paragraphs** — nodes are labels/phrases only. If you encounter a long paragraph in the source, distill it into tight bullet points covering all its key ideas.

7. After creating the file, tell the user:
   - The exact output path.
   - How to open it as a mind map in Obsidian (right-click the file → "Open as Mind Map", or just open it — Markmind auto-detects the frontmatter).
   - That they can also open it in Outline or Table mode via the "More options" (⋮) menu in Obsidian.
   - Export options: `Ctrl+P` → "Export to HTML" or "Export mindmap as a PDF file".

---

### Step 4 — Review and iterate

After delivering the file:
1. **Always ask for feedback** — don't just say "done" and stop. Say something like: "افتح الملف في الـ Obsidian وشوفه كـ mind map — عايز تغيّر حاجة في الـ structure أو الـ styling؟ ولا في محتوى معين محتاج تضيفه أو تحذفه؟"
2. **Iterate directly** — if the user wants changes (regroup branches, rename nodes, add emoji, adjust depth), edit the file in place; don't regenerate from scratch.
3. **Merge new sources** — if the user points to more files to add, read them and merge their content as new `##` branches into the existing output file.
4. **Confirm each change** — after editing, tell the user exactly what changed: "عدّلت الـ branch X وأضفت Y nodes جديدة — بص عليها تاني."

---

## Hard Rules

- **Never use `mindmap-plugin: rich`** — this skill only produces Basic mode files. Rich mode stores JSON data and is not human-editable.
- **Never put prose paragraphs as node text** — nodes must be concise labels/phrases. Long text breaks the mind map layout.
- **Never use multiple `# H1` headings in a single output file** — only one root node per mind map file.
- **Never invent content** — every node must come from the actual source file(s). Don't add topics that weren't in the source.
- **Never translate technical terms — ever, under any circumstances, even in Arabic mode.** `API`, `hook`, `state`, `component`, `render`, `function`, `loop`, `framework`, `plugin`, `node`, `branch` — these and all other established English technical terms must appear in English in every node, heading, and label. Arabic mode means Arabic *explanations*, never Arabic *term replacements*.
- **Never omit content** — the mind map must cover all meaningful information from the source, not just highlights. Completeness is mandatory.
- **Always apply visual styling** — emoji branch icons, bold key terms, inline code for identifiers. A plain unstyled mind map is not acceptable output for this skill.
- **Never skip Step 0, and always ask for the source location first** — it is the very first message the skill sends, no exceptions.
- **Always confirm understanding at the end of Step 0** before proceeding to reading any files.
- **Always tell the user the exact output path** (folder + filename) immediately after creating the file.
- **Always ask for feedback after delivering** — never end the interaction with just "done".
- **Filenames must follow the inferred naming convention** from the source folder — never impose a fixed style. If the convention cannot be determined, default to kebab-case.
- **Never nest deeper than 4 levels** — Markmind Basic mode becomes hard to read beyond that.
- **Always include the `mindmap-plugin: basic` frontmatter** — without it, the file is just a regular Markdown note and Markmind won't recognize it.

---

## Reference: Full Example Output

Below is a complete example of what a valid output file looks like, for a source note about "React Hooks":

```markdown
---
mindmap-plugin: basic
tags: [mind-map, react, hooks]
source: "[[react-hooks-notes]]"
created: 2026-07-27
---

# الـ React Hooks

## 💡 إيه هي الـ Hooks؟
- **بديلة** الـ class components في الـ React
- بتخلي الـ functional components تتحكم في الـ state
- متاحة من الـ **React 16.8**

## ⚙️ أهم الـ Hooks الأساسية
### الـ useState
- بتخزّن الـ **state** جوه الـ component
- بترجع array فيها القيمة ودالة التعديل
- `const [count, setCount] = useState(0)`

### الـ useEffect
- بتشتغل بعد كل **render**
- بتستخدمها للـ side effects (API calls, subscriptions)
- `[]` كـ dependency = بتشتغل مرة واحدة بس

### الـ useContext
- بتوصلك للـ **Context** بدون prop drilling
- أسهل من الـ Consumer القديم

## ⚠️ قواعد الـ Hooks (Rules of Hooks)
- استخدمها في الأعلى بس (**top level**)
- متستخدمهاش جوه conditions أو loops
- شغّلها في الـ React functions بس

## 🛠️ متى تعمل Custom Hook؟
- لما **منطق بيتكرر** في أكتر من component
- اسمها لازم تبدأ بـ `use`
- [[custom-hooks-notes]]
```

---

## References

- [Obsidian Markmind GitHub](https://github.com/MarkMindCkm/obsidian-markmind)
- [Markmind Official Website](https://www.markmind.net)
- [Obsidian Stats — Markmind Plugin](https://www.obsidianstats.com/plugins/obsidian-markmind)
- [Markmind Docs — Basic Mode](https://markmindckm.github.io/markmind-docs/index.html#/basic)
- [Markmind Docs — Outline Mode](https://markmindckm.github.io/markmind-docs/index.html#/outline)
- [Markmind Docs — Table Mode](https://markmindckm.github.io/markmind-docs/index.html#/table)
- [Markmind Docs — Embed Mind Map](https://markmindckm.github.io/markmind-docs/index.html#/embed)
- [YouTube: How to use basic mode of MindMap](https://www.youtube.com/watch?v=7SkIHeQOI44)
- [YouTube: How to use markdown mode of MindMap](https://www.youtube.com/watch?v=87dnyg4vEBo)
