# opencode-skills

> Custom [OpenCode](https://opencode.ai) skills that turn your AI agent into a full-featured programming tutor and Obsidian productivity tool.

## Overview

This repository contains drop-in skills for [OpenCode](https://opencode.ai) — an AI-powered coding assistant. Each skill is a self-contained Markdown instruction set that teaches the agent a new specialized workflow. Install by cloning into `~/.config/opencode/skills/`.

## Available Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| **study-programming** | Interactive programming tutor with spaced repetition, Socratic exercises, and progress tracking — teaches in Egyptian Arabic with English technical terms | `"teach me Python"`, `"I want to learn React"` |
| **convert-to-mind-map** | Converts Markdown notes into interactive Obsidian Markmind visual maps | `"convert this folder to a mind map"` |

---

### study-programming

A full learning system that takes a learner from absolute zero to professional-level mastery of any programming language, framework, or tech topic.

**Features:**
- 3-level structured roadmap (Beginner -> Intermediate -> Advanced)
- Lesson-by-lesson teaching in Egyptian Arabic mixed with English technical terms
- Mandatory exercises after every lesson with Socratic hinting (no answer-dropping)
- Confidence scoring, misconception logging, and progress tracking in a single file
- Spaced-repetition reviews at the start of every session
- Level capstone projects combining all taught concepts
- References section with real sources at the end of every lesson

**Core principles:**
- Zero-assumption teaching — every concept is explained from scratch
- No lesson proceeds until the previous exercise is passed
- Technical terms are never translated — always kept in English
- All code blocks are 100% English, no exceptions

---

### convert-to-mind-map

Reads existing Markdown notes from any folder and produces ready-to-open [Markmind](https://github.com/MarkMindCkm/obsidian-markmind)-compatible mind map files for Obsidian.

**Features:**
- Reads one or more Markdown files from a user-specified folder
- Analyzes content structure and groups related ideas into a clean hierarchy
- Produces `.md` files with `mindmap-plugin: basic` frontmatter
- Human-readable, bidirectional, zero manual work

---

## Installation

```bash
# Clone into your OpenCode skills directory
cd ~/.config/opencode/skills/
git clone https://github.com/nagdista-dev/opencode-skills.git
```

Or copy any skill folder manually into `~/.config/opencode/skills/`.

## Requirements

- [OpenCode](https://opencode.ai) CLI installed
- (Optional) [Obsidian](https://obsidian.md) with the [Markmind](https://github.com/MarkMindCkm/obsidian-markmind) plugin for mind map features

## Contributing

Contributions are welcome. Open an issue or submit a pull request with a new skill or improvements to existing ones. Each skill should follow the structure:

```
skill-name/
├── SKILL.md          # Main skill instructions
└── references/       # Templates, examples, or supporting files (optional)
```

## License

MIT
