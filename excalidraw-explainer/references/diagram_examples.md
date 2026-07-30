# Diagram JSON Examples

Minimal but complete working examples for each diagram type.
These serve as the ground truth for valid .excalidraw JSON structure.
All IDs are illustrative — always generate fresh unique IDs in real output.

---

## How to Read These Examples

Every example shows the `elements` array only.
Wrap it in the full root structure:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ ...paste elements here... ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null,
    "exportWithDarkMode": false
  },
  "files": {}
}
```

---

## Example 1 — Flowchart (3 steps + 1 decision)

Topic: Boiling Water

```json
[
  {
    "id": "ell_start_001xyzABCDEFGHIJ",
    "type": "ellipse",
    "x": 300, "y": 50,
    "width": 200, "height": 70,
    "angle": 0,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "#d0bfff",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "roundness": { "type": 2 },
    "seed": 123456781,
    "version": 1,
    "versionNonce": 987654321,
    "isDeleted": false,
    "boundElements": [{ "type": "text", "id": "txt_start_001abcDEFGHIJKL" }],
    "updated": 1700000000000,
    "link": null,
    "locked": false
  },
  {
    "id": "txt_start_001abcDEFGHIJKL",
    "type": "text",
    "x": 310, "y": 72,
    "width": 180, "height": 26,
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
    "seed": 223344556,
    "version": 1,
    "versionNonce": 667788990,
    "isDeleted": false,
    "boundElements": [],
    "updated": 1700000000000,
    "link": null,
    "locked": false,
    "text": "Start",
    "fontSize": 18,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "ell_start_001xyzABCDEFGHIJ",
    "originalText": "Start",
    "autoResize": true
  },
  {
    "id": "arr_001_to_002_mno789PQR",
    "type": "arrow",
    "x": 400, "y": 120,
    "width": 0, "height": 80,
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
    "roundness": { "type": 2 },
    "seed": 334455667,
    "version": 1,
    "versionNonce": 778899001,
    "isDeleted": false,
    "boundElements": [],
    "updated": 1700000000000,
    "link": null,
    "locked": false,
    "points": [[0, 0], [0, 80]],
    "startBinding": { "elementId": "ell_start_001xyzABCDEFGHIJ", "focus": 0, "gap": 8 },
    "endBinding": { "elementId": "rec_step1_002uvwXYZabcdef", "focus": 0, "gap": 8 },
    "startArrowhead": null,
    "endArrowhead": "arrow"
  },
  {
    "id": "rec_step1_002uvwXYZabcdef",
    "type": "rectangle",
    "x": 300, "y": 200,
    "width": 200, "height": 70,
    "angle": 0,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "#a5d8ff",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "strokeStyle": "solid",
    "roughness": 1,
    "opacity": 100,
    "groupIds": [],
    "frameId": null,
    "roundness": { "type": 3 },
    "seed": 445566778,
    "version": 1,
    "versionNonce": 889900112,
    "isDeleted": false,
    "boundElements": [{ "type": "text", "id": "txt_step1_002ghiJKLMNOpqr" }],
    "updated": 1700000000000,
    "link": null,
    "locked": false
  },
  {
    "id": "txt_step1_002ghiJKLMNOpqr",
    "type": "text",
    "x": 310, "y": 222,
    "width": 180, "height": 26,
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
    "seed": 556677889,
    "version": 1,
    "versionNonce": 990011223,
    "isDeleted": false,
    "boundElements": [],
    "updated": 1700000000000,
    "link": null,
    "locked": false,
    "text": "Fill pot with water",
    "fontSize": 18,
    "fontFamily": 1,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "rec_step1_002uvwXYZabcdef",
    "originalText": "Fill pot with water",
    "autoResize": true
  }
]
```

> This snippet shows 2 shapes + 1 arrow. Scale the pattern for more steps.

---

## Example 2 — Mind Map Node Pattern

Each branch = center ellipse + branch rectangle + connecting line.

```json
{
  "id": "lin_center_to_b1_stuvWXYZabc",
  "type": "line",
  "x": 540, "y": 390,
  "width": 260, "height": 240,
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
  "roundness": { "type": 2 },
  "seed": 667788901,
  "version": 1,
  "versionNonce": 101213141,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "points": [[0, 0], [260, -240]],
  "startArrowhead": null,
  "endArrowhead": null
}
```

> Lines (not arrows) connect center to branches in mind maps — no arrowheads.

---

## Example 3 — Standalone Arrow Label (for Concept Maps)

Place a small text element at the midpoint of an arrow to label the relationship.

```json
{
  "id": "txt_label_arrow_relXYZpqrstu",
  "type": "text",
  "x": 425, "y": 295,
  "width": 120, "height": 20,
  "angle": 0,
  "strokeColor": "#555555",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 778899012,
  "version": 1,
  "versionNonce": 121314151,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "text": "causes",
  "fontSize": 14,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "causes",
  "autoResize": true
}
```

---

## ID Generation Pattern

Generate IDs that look like: `rec_` + 3-char role prefix + `_` + sequential 3-digit + 12-char random.

Examples:
```
rec_stp_001aBcDeFgHiJkL   ← rectangle, step, index 001
ell_ctr_001mNoPqRsTuVwX   ← ellipse, center
arr_001_002xYzAbCdEfGhI   ← arrow from element 001 to 002
txt_stp_001jKlMnOpQrStU   ← text bound to step 001
lin_bkb_001vWxYzAbCdEfG   ← line, backbone
dmd_dec_001hIjKlMnOpQrS   ← diamond, decision
```

This makes planning and cross-referencing IDs much easier.
