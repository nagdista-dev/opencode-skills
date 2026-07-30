# Color Themes Reference

Full color palette definitions for all 5 themes.
The AI reads this file when selecting colors for any diagram element.

---

## How to Apply Themes

For each diagram element, assign colors based on its **role**:

| Role | Description |
|---|---|
| `primary` | Main steps, primary nodes, main branches |
| `secondary` | Sub-steps, child nodes, secondary branches |
| `accent` | Highlighted or important elements |
| `decision` | Diamond shapes in flowcharts |
| `start_end` | Start/End ellipses in flowcharts |
| `text` | All text stroke color (labels inside shapes) |
| `stroke` | All shape border/outline color |
| `bg` | Canvas background color |

---

## Theme A — Light (Default)

```json
{
  "viewBackgroundColor": "#ffffff",
  "exportWithDarkMode": false,
  "roles": {
    "stroke":    "#1e1e1e",
    "text":      "#1e1e1e",
    "primary":   "#a5d8ff",
    "secondary": "#b2f2bb",
    "accent":    "#ffec99",
    "decision":  "#ffd8a8",
    "start_end": "#d0bfff"
  }
}
```

**Usage:** Clean, professional. Best for general-purpose diagrams and printed output.

---

## Theme B — Colorful

```json
{
  "viewBackgroundColor": "#ffffff",
  "exportWithDarkMode": false,
  "roles": {
    "stroke":     "#1e1e1e",
    "text":       "#1e1e1e",
    "category_1": "#ff6b6b",
    "category_2": "#4ecdc4",
    "category_3": "#45b7d1",
    "category_4": "#96ceb4",
    "category_5": "#ffeaa7",
    "category_6": "#dda0dd"
  }
}
```

**Usage:** Assign one category color per branch or section. Rotate through categories for each new top-level node. Best for Mind Maps and Concept Maps.

---

## Theme C — Dark

```json
{
  "viewBackgroundColor": "#1e1e2e",
  "exportWithDarkMode": true,
  "roles": {
    "stroke":    "#cdd6f4",
    "text":      "#cdd6f4",
    "primary":   "#313244",
    "secondary": "#45475a",
    "accent":    "#89b4fa",
    "decision":  "#585b70",
    "start_end": "#7287fd"
  }
}
```

**Usage:** Dark Catppuccin-inspired palette. All `strokeColor` and text values must use `#cdd6f4` (not `#1e1e1e`). Best for night-study sessions.

---

## Theme D — Warm

```json
{
  "viewBackgroundColor": "#fff9f0",
  "exportWithDarkMode": false,
  "roles": {
    "stroke":    "#5c2d00",
    "text":      "#5c2d00",
    "primary":   "#ff9a3c",
    "secondary": "#ffd194",
    "accent":    "#ff6b35",
    "decision":  "#ffb347",
    "start_end": "#ffe0b2"
  }
}
```

**Usage:** Energetic, warm tones. Great for history timelines, creative topics, and motivational content.

---

## Theme E — Cool

```json
{
  "viewBackgroundColor": "#f0f7ff",
  "exportWithDarkMode": false,
  "roles": {
    "stroke":    "#0d3349",
    "text":      "#0d3349",
    "primary":   "#0d9488",
    "secondary": "#a5d8ff",
    "accent":    "#38bdf8",
    "decision":  "#67e8f9",
    "start_end": "#bae6fd"
  }
}
```

**Usage:** Calm, focused. Ideal for scientific topics, technical architecture, and medical content.

---

## Font Family Values

| Value | Font |
|---|---|
| `1` | Virgil (default hand-drawn Excalidraw font) |
| `2` | Helvetica |
| `3` | Cascadia (monospace) |

**Always use `fontFamily: 1`** (Virgil) to maintain the hand-drawn aesthetic.

---

## Font Size Guidelines

| Use Case | fontSize |
|---|---|
| Title / Main node label | 24 |
| Standard node label | 18 |
| Sub-node label | 16 |
| Small annotation / number label | 14 |
| Arrow relationship label | 14 |
