# Markmind Plugin — Reference

> Read this file when you need detailed knowledge about Markmind's file format, syntax, or features.

---

## What is Markmind?

Markmind is an Obsidian community plugin (by MarkMindCkm) that turns a specially-formatted `.md` file into an interactive, visual mind map inside Obsidian. It supports two modes:

| Mode | How it stores data | Best for |
|---|---|---|
| **Basic** | Pure Markdown (headings + bullet lists) | Simple, readable, human-editable maps |
| **Rich** | JSON embedded in the file | Advanced layouts: summaries, boundaries, free nodes, colors |

**This skill always uses Basic mode.** Rich mode is JSON-heavy, not human-editable, and out of scope.

---

## Basic Mode File Format

A valid Markmind Basic mode file **must** start with:

```yaml
---
mindmap-plugin: basic
---
```

### Hierarchy mapping

| Markdown element | Mind map role |
|---|---|
| `# Heading 1` | Root / central node (only ONE per file) |
| `## Heading 2` | First-level branch |
| `### Heading 3` | Second-level branch |
| `- bullet` | Child node |
| `  - indented bullet` | Nested child |

### What renders inside nodes (supported inline Markdown)

- Bold: `**text**`
- Italic: `*text*`
- Strikethrough: `~~text~~`
- Inline code: `` `code` ``
- Wikilinks: `[[note]]`
- KaTeX math: `$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$`
- Emojis: standard Unicode characters ✅

### What does NOT render as nodes (avoid inside map body)

- Tables
- Callouts (`> [!note]`)
- Code fences (` ``` `)
- Horizontal rules

### Checkboxes

`- [ ]` and `- [x]` render as toggleable task nodes in the mind map view.

### Bidirectional sync

Edits in the text editor update the mind map view and vice versa.

---

## Optional Display Modes

Add `display-mode` to frontmatter to change the view:

| display-mode value | What it shows |
|---|---|
| *(none — default)* | Mind map view |
| `outline` | Collapsible hierarchical outline |
| `table` | Spreadsheet-like table view |

Example:
```yaml
---
mindmap-plugin: basic
display-mode: outline
---
```

The user can also switch view via the "More options" (⋮) menu in Obsidian without changing the frontmatter.

---

## Embedding a Mind Map in Another Note

```markdown
![[mind-map-filename]]
```

This renders the interactive mind map inline inside the host note.

---

## Export Options (via `Ctrl+P`)

- **Export to HTML** — produces a standalone HTML file.
- **Export mindmap as a PDF file** — requires the map to be open in an independent window first.

---

## AI Generation (Advanced)

Markmind 3.5+ supports AI-generated mind maps via:
- `Ctrl+P` → "Generate mind maps by ChatGPT"
- Configurable with custom AI endpoints (e.g. DeepSeek, OpenAI)

This skill does NOT use this feature — the AI (this agent) does the generation directly.

---

## Links

- [GitHub](https://github.com/MarkMindCkm/obsidian-markmind)
- [Official website](https://www.markmind.net)
- [Obsidian Stats page](https://www.obsidianstats.com/plugins/obsidian-markmind)
- [Docs — Basic Mode](https://markmindckm.github.io/markmind-docs/index.html#/basic)
- [Docs — Outline Mode](https://markmindckm.github.io/markmind-docs/index.html#/outline)
- [Docs — Table Mode](https://markmindckm.github.io/markmind-docs/index.html#/table)
- [Docs — Embed](https://markmindckm.github.io/markmind-docs/index.html#/embed)
- [YouTube: Basic mode tutorial](https://www.youtube.com/watch?v=7SkIHeQOI44)
- [YouTube: Markdown mode tutorial](https://www.youtube.com/watch?v=87dnyg4vEBo)
- [YouTube: Rich mode tutorial](https://youtu.be/ajg2VWol0L4)
