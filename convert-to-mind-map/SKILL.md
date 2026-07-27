---
name: convert-to-mind-map
description: Use this skill whenever the user wants to convert one or more Markdown files into an Obsidian Markmind mind map (e.g. "حوّل الملف ده لـ mind map", "عايز أعمل mind map من الـ notes دي", "Convert this to a mind map", "اعمللي mind map من الفولدر ده"). This skill reads existing Markdown files from a user-specified folder, intelligently analyzes their content and structure, and produces ready-to-open Markmind-compatible `.md` files (using `mindmap-plugin: basic` frontmatter) inside the same vault. ALWAYS use this skill (not a generic explanation) whenever the user asks to convert notes, files, or a folder into a mind map, visual map, or Markmind board — even if they don't say the word "skill" explicitly.
---

# Convert to Mind Map — Obsidian Markmind Skill

## What This Skill Does

This skill reads one or more existing Markdown notes from a folder the user points to, then produces a well-structured Markmind-compatible mind map file (`.md`) that Obsidian can open directly as a visual mind map using the **Markmind plugin** (Basic mode). The AI does the heavy lifting: it reads, understands, groups, and restructures the content into a clean hierarchy — the user gets a ready-to-open mind map with zero manual work.

---

## Plugin Background — Obsidian Markmind

Before doing any work, the AI must understand how Markmind works so it produces correct, openable files.

### What is Markmind?

Markmind is an Obsidian community plugin (by MarkMindCkm) that turns a specially-formatted `.md` file into an interactive, visual mind map inside Obsidian. It supports two modes:

| Mode | How it stores data | Best for |
|---|---|---|
| **Basic** | Pure Markdown (headings + bullet lists) | Simple, readable, human-editable maps |
| **Rich** | JSON embedded in the file | Advanced layouts: summaries, boundaries, free nodes, colors |

**This skill always uses Basic mode** — it produces clean, human-readable Markdown that syncs bidirectionally with the mind map view. Rich mode is JSON-heavy and not human-editable, so it is out of scope here.

---

### Basic Mode File Format

A valid Markmind Basic mode file **must** have this frontmatter:

```yaml
---
mindmap-plugin: basic
---
```

After the frontmatter, the mind map structure is represented entirely using standard Markdown headings and bullet lists:

```markdown
---
mindmap-plugin: basic
---

# Root Node (the central topic)

## Branch 1 (first-level branch)
- Child node 1.1
- Child node 1.2
  - Nested child 1.2.1
  - Nested child 1.2.2

## Branch 2 (second-level branch)
- Child node 2.1
  - [ ] Task node (with checkbox)
  - [ ] Another task

## Branch 3
- Child with **bold** emphasis
- Child with `inline code`
- Child with [[wikilink to another note]]
- Child with $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$ (KaTeX math)
```

**Hierarchy mapping:**

| Markdown element | Mind map role |
|---|---|
| `# Heading 1` | Root/central node |
| `## Heading 2` | First-level branch |
| `### Heading 3` | Second-level branch (sub-branch) |
| `- bullet` | Child node under the nearest heading/bullet above it |
| `  - indented bullet` | Nested child (deeper level) |

**Important rules for valid Basic mode files:**

1. **Only one `# H1`** — this becomes the root/center node of the mind map. Never use multiple H1s in the same file.
2. **`##` and `###` headings** create named branches; bullet lists under them create child nodes.
3. **Synced bidirectionally** — edits in the text editor update the mind map view and vice versa.
4. **Supported inline Markdown in nodes:** bold (`**text**`), italic (`*text*`), strikethrough (`~~text~~`), inline code (`` `code` ``), wikilinks (`[[note]]`), KaTeX math (`$formula$`), emojis (standard Unicode).
5. **Checkboxes work** — `- [ ]` and `- [x]` render as toggleable task nodes inside the mind map view.
6. **No tables, no callouts, no code fences** — these do not render as mind map nodes; avoid putting them inside the mind map body.
7. **Node text should be concise** — mind map nodes are designed for short phrases, not full paragraphs. Summarize, don't paste.

---

### Display Modes (Optional Frontmatter)

Beyond the basic mind map view, a Basic mode file can also be opened in:

| Display mode | Frontmatter to add | What it shows |
|---|---|---|
| Outline | `display-mode: outline` | A collapsible hierarchical outline (like WorkFlowy) |
| Table | `display-mode: table` | The hierarchy displayed as a spreadsheet-like table |

Example for outline mode:

```yaml
---
mindmap-plugin: basic
display-mode: outline
---
```

The AI **does not** need to set these — the default (no `display-mode`) opens as a mind map. Mention them to the user as an option.

---

### Embedding a Mind Map in Another Note

A Markmind mind map can be embedded inside any other Obsidian note using:

```markdown
![[mind-map-filename]]
```

This renders the interactive mind map inline inside the host note. The AI should mention this to the user when relevant.

---

### Export Options

From within Obsidian, a Markmind mind map can be exported via `Ctrl+P`:
- **Export to HTML** — produces a standalone HTML file with the mind map.
- **Export as PDF** — requires opening the map in an independent window first, then using the command.

The AI should inform the user of these options after creating the file.

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
| **Arabic** | Write all node labels in Arabic. Technical terms (e.g. `useState`, `API`, `render`) stay in English as-is — do not translate them. Apply the RTL flow rule: if a node label would start with a bare English term, prepend "الـ" (e.g. "الـ useState hook"). |
| **English** | Write all node labels in English. Keep them concise and clear. |

**Key rule for Arabic mode:** same as the `study-programming` skill — technical terms never get translated. You explain their meaning in Arabic prose, but the term itself stays English. A node like `- الـ useEffect بتشتغل بعد كل render` is correct; a node like `- خطاف التأثير بيشتغل بعد كل تصيير` is wrong.

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

**Interactivity rule for Step 0:** After the user answers all three questions, confirm back what you understood before proceeding — e.g. "تمام، هقرأ الفولدر X، هعمل mind map واحد للكل، بالعربي، وهحفظه في نفس الفولدر. نبدأ؟" — and wait for confirmation.

---

### Step 1 — Read and analyze the source files

For each source Markdown file:
1. Read the full content.
2. Identify the main topic/title (from the `# H1`, the `title:` frontmatter field, or the filename — in that order of priority).
3. Extract the key concepts, sections, and sub-points. Strip out prose filler — you're extracting *structure and key ideas*, not copying paragraphs.
4. Note any existing headings (`##`, `###`) — these become natural branches.
5. Note any existing lists — these become child nodes.
6. Note any wikilinks `[[...]]` inside the source — preserve them as-is in the mind map nodes; they stay clickable in Obsidian.
7. Note the source file's frontmatter properties (tags, aliases, dates) — you may use tags as branch labels if relevant.

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

1. **Filename:** Use English kebab-case: `<source-slug>-mindmap.md` (e.g., `react-hooks-mindmap.md`). If combining multiple files, use a descriptive kebab-case name for the collection (e.g., `project-overview-mindmap.md`). The file is always saved in the **same folder** as the source file(s) — never in a different location.

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
- **Never omit content** — the mind map must cover all meaningful information from the source, not just highlights. Completeness is mandatory.
- **Always apply visual styling** — emoji branch icons, bold key terms, inline code for identifiers. A plain unstyled mind map is not acceptable output for this skill.
- **Never skip Step 0, and always ask for the source location first** — it is the very first message the skill sends, no exceptions.
- **Always confirm understanding at the end of Step 0** before proceeding to reading any files.
- **Always tell the user the exact output path** (folder + filename) immediately after creating the file.
- **Always ask for feedback after delivering** — never end the interaction with just "done".
- **Filenames are English kebab-case only** — no Arabic, no spaces, no special characters.
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
