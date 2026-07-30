---
name: excalidraw-explainer
description: >
  Converts any topic or Markdown note into a ready-to-open .excalidraw diagram
  file for the Obsidian Excalidraw plugin. Supports two input modes: (1) a free
  topic the user describes in text, or (2) a path to an existing Markdown file
  the AI reads and converts. Always asks smart multiple-choice questions first
  (language, diagram type, color theme, detail level, save path) before generating.
  Generates valid .excalidraw JSON and writes it directly to the Obsidian vault.
  Trigger: "explain with excalidraw", "make a diagram", "visualize this topic",
  "convert this note to excalidraw", "draw a diagram for", "use excalidraw-explainer",
  "اشرح بـ excalidraw", "ارسم diagram", "حوّل الملف لـ excalidraw", or any request
  to visually explain or diagram any topic using Excalidraw.
license: MIT
compatibility: opencode
allowed-tools: [Read, Write, WebSearch]
metadata:
  audience: students-learners
  workflow: visual-learning
  output: .excalidraw
---

# Excalidraw Explainer

Transforms any topic or Markdown note into a structured, visually rich `.excalidraw` diagram saved directly into the user's Obsidian vault. The file opens natively in the Obsidian Excalidraw plugin with no extra steps.

> **Core Rule:** Understand first. Ask second. Generate last. Never skip steps.

---

## Reference Files

> [!IMPORTANT]
> Before starting any session, check for these reference files and load them if they exist:
> - `references/diagram_examples.md` — valid JSON examples for each diagram type
> - `references/color_themes.md` — complete color palette definitions
> - `examples/` — real .excalidraw output samples to calibrate quality

---

## Input Mode Detection

On every activation, silently determine which input mode the user is using:

| Signal | Mode |
|---|---|
| User describes a topic in text | **Mode A — Free Topic** |
| User provides a `.md` file path | **Mode B — Markdown File** |
| User shares raw text/notes inline | **Mode A — treat as free topic** |

---

## Step 0 — Understand Before Asking

### Mode A — Free Topic

Silently before asking anything:

1. Identify the core topic and its domain (science, history, programming, business, etc.)
2. Assess complexity — single concept, multi-step process, system of parts, or comparison?
3. Map likely sub-concepts that must appear in the diagram
4. If the topic is technical or unfamiliar → **run a web search first**
5. Pre-select the best-fitting diagram type (you'll suggest it in Step 1)

### Mode B — Markdown File

If the user provides a `.md` path:

1. **Read the file immediately** using the Read tool — do not ask what it contains
2. Silently analyze:
   - Main topic (usually `# heading` or first paragraph)
   - Section structure (`## headings` → diagram branches/nodes)
   - Type of content: sequential steps, comparisons, definitions, timeline events?
3. Map each `##` heading to a major diagram node
4. Select the diagram type that best fits the file structure:

| File Structure | Best Diagram Type |
|---|---|
| Numbered steps or procedures | Step-by-step or Flowchart |
| Multiple independent sections | Mind Map or Concept Map |
| Two or more items being compared | Comparison |
| Dates, events, periods | Timeline |
| Complex interlinking ideas | Concept Map |
| Decision branching | Flowchart |

5. In Step 1, mark your recommended type with ✅ but let the user override

Do **not** generate anything. Do **not** show this analysis to the user.

---

## Step 1 — Discovery Questions (Single Message)

Send **all questions in one message**. User replies with one letter per question line.
Fast, scannable, no back-and-forth.

### Format — Mode A (Free Topic)

```
Got it — before I draw anything, I need a few quick choices:

1️⃣  Diagram language?
    a) Arabic (العربية)
    b) English
    c) Mixed (Arabic labels + English technical terms)

2️⃣  Diagram type?
    a) Flowchart       — steps, decisions, branching paths
    b) Mind Map        — central idea with radiating branches
    c) Step-by-Step    — numbered sequence of clear stages
    d) Comparison      — side-by-side comparison of two or more items
    e) Timeline        — chronological sequence of events
    f) Concept Map     — interconnected concepts with labeled relationships

3️⃣  Level of detail?
    a) Quick overview   (5–8 nodes)
    b) Standard         (10–18 nodes)
    c) Deep dive        (20–35 nodes)

4️⃣  Color theme?
    a) Light      — white background, soft blue accents (default)
    b) Colorful   — distinct color per section/branch
    c) Dark       — dark background, light strokes
    d) Warm       — orange, red, gold tones
    e) Cool       — teal, blue, green tones

5️⃣  Save path in your Obsidian vault?
    (Type the full folder path, or type "default" to save in the vault root)

Reply like: 1b 2a 3b 4c 5/path/to/folder
```

### Format — Mode B (Markdown File)

```
Read the file ✅ — a few quick choices before I generate:

1️⃣  Diagram language?
    a) Arabic (العربية)
    b) English
    c) Mixed (Arabic labels + English technical terms)

2️⃣  Diagram type?  (I suggest: [TYPE] ✅ — based on the file structure)
    a) Flowchart       — steps, decisions, branching paths
    b) Mind Map        — central idea with radiating branches
    c) Step-by-Step    — numbered sequence of clear stages
    d) Comparison      — side-by-side comparison of two or more items
    e) Timeline        — chronological sequence of events
    f) Concept Map     — interconnected concepts with labeled relationships

3️⃣  Color theme?
    a) Light      — white background, soft blue accents (default)
    b) Colorful   — distinct color per section/branch
    c) Dark       — dark background, light strokes
    d) Warm       — orange, red, gold tones
    e) Cool       — teal, blue, green tones

4️⃣  Save path in your Obsidian vault?
    (Default: same folder as the source .md file — type "default" or provide a path)

Reply like: 1b 2a 3c 4default
```

Wait for the user's reply. Do not proceed without it.

---

## Step 2 — Confirm Before Generating

After receiving the user's answers, show a brief confirmation summary:

```
Here's what I'll build:

📊  Type:     [diagram type]
🌐  Language: [language]
🎨  Theme:    [color theme]
🔍  Detail:   [detail level]          ← (Mode A only)
📁  Save to:  [resolved full path]
📄  Filename: [topic-name.excalidraw]

Start? (y / yes / go)
```

**Resolve the filename** as:
- Translate the topic to English if needed
- Convert to lowercase kebab-case
- Append `.excalidraw`
- Examples: `water-cycle.excalidraw` | `http-request-lifecycle.excalidraw` | `photosynthesis-steps.excalidraw`

Wait for confirmation. Never generate without it.

---

## Step 3 — Internal Layout Planning (Silent)

Before writing JSON, plan the canvas silently:

1. List every element needed (shape type, label text, x/y position, size)
2. Establish the coordinate grid — reference values:
   - Canvas starts at x=0, y=0
   - Default shape size: rectangles 200×70, diamonds 160×100, ellipses 180×70
   - Vertical spacing between rows: 150px
   - Horizontal spacing between columns: 250px
3. Map connections (which element's id → which element's id)
4. Assign colors from the selected theme to each element role
5. Pre-generate all unique IDs (20-char alphanumeric strings)

---

## Step 4 — Generate the .excalidraw File

### 4.1 Root Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null,
    "exportWithDarkMode": false
  },
  "files": {}
}
```

For **Dark theme**: set `"viewBackgroundColor": "#1e1e2e"` and `"exportWithDarkMode": true`.

### 4.2 Element ID Rules

- Every element must have a **unique 20-character alphanumeric ID**
- Generate random strings — never use sequential IDs like `id-1`, `id-2`
- Valid examples: `"aB3kL9mNpQ2rS5tUvW8x"` | `"Xz7yC4dE6fG1hI0jK3lM"`
- Pre-generate all IDs in planning (Step 3) before writing JSON

### 4.3 Universal Element Properties

Every element, regardless of type, must include:

```json
{
  "id": "<unique-20-char-id>",
  "type": "<shape-type>",
  "x": 0,
  "y": 0,
  "width": 200,
  "height": 70,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 123456789,
  "version": 1,
  "versionNonce": 987654321,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

`seed` and `versionNonce` must be **random 9-digit integers**, different for every element.

### 4.4 Shape Reference

#### Rectangle
```json
{
  "type": "rectangle",
  "width": 200,
  "height": 70,
  "roundness": { "type": 3 }
}
```

#### Diamond (decisions in flowcharts)
```json
{
  "type": "diamond",
  "width": 160,
  "height": 100,
  "roundness": null
}
```

#### Ellipse (start/end nodes, mind map center)
```json
{
  "type": "ellipse",
  "width": 200,
  "height": 70,
  "roundness": { "type": 2 }
}
```

#### Line (dividers, timeline backbone)
```json
{
  "type": "line",
  "x": 50,
  "y": 300,
  "width": 800,
  "height": 0,
  "points": [[0, 0], [800, 0]],
  "startArrowhead": null,
  "endArrowhead": null,
  "roundness": null
}
```

#### Arrow (connections between elements)
```json
{
  "type": "arrow",
  "x": 300,
  "y": 85,
  "width": 0,
  "height": 80,
  "points": [[0, 0], [0, 80]],
  "startBinding": {
    "elementId": "<source-element-id>",
    "focus": 0,
    "gap": 8
  },
  "endBinding": {
    "elementId": "<target-element-id>",
    "focus": 0,
    "gap": 8
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "roundness": { "type": 2 }
}
```

Arrow points describe the path **relative to the arrow's own x,y origin**.
For a straight down arrow of 80px: `"points": [[0, 0], [0, 80]]`
For a straight right arrow of 150px: `"points": [[0, 0], [150, 0]]`
When `startBinding`/`endBinding` are not needed: set both to `null`.

#### Standalone Text
```json
{
  "type": "text",
  "x": 100,
  "y": 50,
  "width": 200,
  "height": 24,
  "text": "Label Text",
  "fontSize": 18,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Label Text",
  "autoResize": true
}
```

### 4.5 Bound Text (Text Inside a Shape)

**Critical rule:** When a shape contains text, you must create TWO elements:
1. The shape with `boundElements` referencing the text ID
2. The text element with `containerId` set to the shape's ID

```json
// 1 — Shape element
{
  "id": "rect_abc123def456ghi78",
  "type": "rectangle",
  "x": 100, "y": 200,
  "width": 200, "height": 70,
  "boundElements": [
    { "type": "text", "id": "text_xyz789uvw012pqr34" }
  ],
  ...all other universal properties...
}

// 2 — Bound text element
{
  "id": "text_xyz789uvw012pqr34",
  "type": "text",
  "x": 110, "y": 220,
  "width": 180, "height": 30,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 112233445,
  "version": 1,
  "versionNonce": 556677889,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "text": "Shape Label",
  "fontSize": 18,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "rect_abc123def456ghi78",
  "originalText": "Shape Label",
  "autoResize": true
}
```

**Text position inside shape:** `x = shape.x + 10`, `y = shape.y + (shape.height/2 - fontSize/2)`

---

## Step 5 — Diagram Layout Templates

Reference `references/diagram_examples.md` for full JSON examples.

### Flowchart

```
             [Start — Ellipse]          y=50,  x=300
                    ↓ arrow (80px)
           [Step 1 — Rectangle]         y=200, x=200
                    ↓ arrow (80px)
          [Decision — Diamond]          y=350, x=210
          ↙ Yes                ↘ No
  [Step 2a — Rect]        [Step 2b — Rect]
  y=500, x=50             y=500, x=500
          ↘                   ↙
            [End — Ellipse]              y=650, x=300
```

- Main axis: x=300 center, branch left x=50, branch right x=550
- Vertical gap between shapes: 130px (gap between bottom edge and arrow start)
- Decision labels: standalone `text` elements placed beside the arrow, not bound

### Mind Map

```
                [Center — Ellipse]       x=450, y=350
               /    |    |    \
         [B1] [B2] [B3] [B4]
```

- Center: large ellipse, width=220, height=80, at x=450, y=350
- 4 branches (adjust per topic): corners at (100,150), (100,550), (800,150), (800,550)
- 6 branches: add (450,50) top and (450,650) bottom
- Use `line` elements (not arrows) from center to branches for organic feel
- Sub-branches extend from each branch node

### Step-by-Step

```
[Step 1] → [Step 2] → [Step 3] → [Step 4]
 x=50        x=300      x=550      x=800
 y=300        y=300      y=300      y=300
```

- Each box: rectangle, width=200, height=70
- Gap between boxes: 50px. Arrow starts at right edge of box (`x = box.x + 200`) and travels 50px right: `points: [[0,0],[50,0]]`
- Arrow `x` position: `box.x + 200`, arrow `y`: `box.y + 35` (vertical center of box)
- Number label: standalone text above each box at `y = box.y - 30`, `x = box.x + 70`, fontSize=14

### Comparison

```
        [Title — top center]
[Item A Header]       [Item B Header]
[Row 1A]  |  [Row 1B]
[Row 2A]  |  [Row 2B]
[Row 3A]  |  [Row 3B]
```

- Vertical divider: `line` element at x=450
- Left column: x=50–400; Right column: x=500–850
- Each row: same y position left and right
- Row height: 80px; start at y=150

### Timeline

```
─────────────────────────────────── (line at y=400, full width)
  │          │          │          │
[E1 above] [E2 below] [E3 above] [E4 below]
```

- Backbone: `line` from x=50 to x=950, y=400
- Connector lines: short vertical `line` elements (40px) at each event x position
- Events alternate above (y=250) and below (y=450) the timeline
- Event box: rectangle, width=160, height=60

### Concept Map

- Place main concepts as rectangles across the canvas (no strict grid)
- Draw `arrow` elements between related concepts
- Label each arrow with a standalone `text` element positioned at the arrow midpoint
- Use `groupIds` to group a shape + its label if needed

---

## Step 6 — Color Themes

Reference `references/color_themes.md` for the full palette.

### Theme A — Light (Default)
```
viewBackgroundColor:  #ffffff
strokeColor:          #1e1e1e
Primary fill:         #a5d8ff   (light blue)
Secondary fill:       #b2f2bb   (light green)
Accent fill:          #ffec99   (yellow)
Decision fill:        #ffd8a8   (peach)
Start/End fill:       #d0bfff   (lavender)
Text color:           #1e1e1e
```

### Theme B — Colorful
```
viewBackgroundColor:  #ffffff
strokeColor:          #1e1e1e
Category 1:           #ff6b6b   (red)
Category 2:           #4ecdc4   (teal)
Category 3:           #45b7d1   (blue)
Category 4:           #96ceb4   (sage green)
Category 5:           #ffeaa7   (yellow)
Category 6:           #dda0dd   (plum)
```

### Theme C — Dark
```
viewBackgroundColor:  #1e1e2e
exportWithDarkMode:   true
strokeColor:          #cdd6f4
Primary fill:         #313244
Secondary fill:       #45475a
Accent fill:          #89b4fa
Text strokeColor:     #cdd6f4
```

### Theme D — Warm
```
viewBackgroundColor:  #fff9f0
strokeColor:          #5c2d00
Primary fill:         #ff9a3c
Secondary fill:       #ffd194
Accent fill:          #ff6b35
Text strokeColor:     #5c2d00
```

### Theme E — Cool
```
viewBackgroundColor:  #f0f7ff
strokeColor:          #0d3349
Primary fill:         #0d9488
Secondary fill:       #a5d8ff
Accent fill:          #38bdf8
Text strokeColor:     #0d3349
```

---

## Step 7 — Save the File

1. Resolve the save path:
   - Mode A + user path: `<user_path>/<filename>.excalidraw`
   - Mode A + "default": Ask the user once: *"What is the full path to your Obsidian vault root?"* — then save at `<vault_root>/<filename>.excalidraw`. Remember this path for the rest of the session.
   - Mode B + "default": same folder as the source `.md` file (extract directory from the file path the user gave)
   - Mode B + user path: `<user_path>/<filename>.excalidraw`

2. Filename: English kebab-case of the topic + `.excalidraw`
   - "دورة الماء" → `water-cycle.excalidraw`
   - "HTTP Request Flow" → `http-request-flow.excalidraw`

3. Write the complete JSON using the **Write** tool.

4. After writing, reply with:

```
✅ Saved to: [full path]

Open Obsidian → navigate to the file → click it.
It will open directly in the Excalidraw plugin.

Want to adjust anything? I can:
  • Add or remove nodes
  • Change the color theme
  • Switch diagram type
  • Translate labels
  • Increase/decrease detail
```

---

## Step 8 — Pre-Save Quality Checklist (Internal — Never Show)

Run this check before calling the Write tool:

- [ ] Root object has `"type": "excalidraw"` and `"version": 2`
- [ ] Every element has a unique 20-char alphanumeric `id`
- [ ] Every shape containing text has TWO elements: shape + bound text
- [ ] Every bound text element has correct `containerId` matching its shape's `id`
- [ ] Every shape's `boundElements` array references its bound text's `id`
- [ ] All arrow `points` arrays start with `[0, 0]`
- [ ] `seed` and `versionNonce` are random 9-digit integers, unique per element
- [ ] Colors match the selected theme exactly
- [ ] Labels are in the chosen language
- [ ] Filename is English kebab-case with `.excalidraw` extension
- [ ] JSON has no trailing commas and no syntax errors
- [ ] Element count matches the selected detail level
- [ ] Root object contains `"files": {}` (required even if empty)
- [ ] Dark theme has `"exportWithDarkMode": true` and correct `viewBackgroundColor`
- [ ] No element has `"type": "text"` with a non-null `containerId` that references a non-existent shape ID

---

## Permanent Rules

1. **Never skip the discovery questions.** No exceptions, no shortcuts.
2. **Never generate without explicit user confirmation** at Step 2.
3. **Always write a complete, syntactically valid `.excalidraw` JSON file** — no partial output, no pseudocode placeholders.
4. **Every shape with text must have a bound text element.** Text never floats independently over shapes.
5. **All IDs must be unique.** If planning reveals a collision, regenerate before writing.
6. **Element count scales with detail level:**
   - Quick overview: 5–10 elements (shapes + texts + arrows combined)
   - Standard: 10–20 elements
   - Deep dive: 20–40 elements
   - Markdown file input: one major diagram node per `##` heading in the source file
7. **Always write the file using the Write tool.** Never print JSON as output and consider it done.
8. **Research unfamiliar topics** with a web search before asking discovery questions.
9. **Mode B: read the file before anything else.** Never ask "what's the topic?" when a file path was provided.
10. **Mode B: preserve the source structure.** Each `##` heading becomes a major node or branch; do not flatten all content into one node.
11. **Always offer revisions** after saving. Diagrams improve iteratively.
12. **Group related elements together.** Every shape + its bound text must share a sub-group ID in `groupIds`. Keep all diagram elements in one main group ID so the whole diagram moves together. Use `["mainGroup", "subGroup"]` pattern.
13. **Z-order: arrows/lines first, shapes second, texts last.** Elements at the beginning of the array render behind elements at the end. Always order elements: arrows → shapes → texts, so connectors stay behind shapes and text is always visible on top.
14. **Code/terminal styling.** When a box represents code, a terminal command, or a CLI operation, use terminal-like styling: `fontFamily: 3` (monospace), `backgroundColor: "#11111b"` (dark terminal bg), `strokeColor: "#585b70"` (subtle border), and `strokeColor: "#a6e3a1"` (green terminal text) for text elements. Non-code boxes retain the default theme styling.
