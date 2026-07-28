# opencode-skills

<p align="center">
  <img src="https://img.shields.io/badge/OpenCode-AI-6B46C1?style=for-the-badge" alt="OpenCode" />
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" alt="Markdown" />
  <img src="https://img.shields.io/badge/Obsidian-7C3AED?style=for-the-badge&logo=obsidian&logoColor=white" alt="Obsidian" />
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License" />
</p>

> Custom [OpenCode](https://opencode.ai) skills that turn your AI agent into a full-featured programming tutor and Obsidian productivity tool.

## Overview

This repository contains drop-in skills for [OpenCode](https://opencode.ai) — an AI-powered coding assistant. Each skill is a self-contained Markdown instruction set that teaches the agent a new specialized workflow. Install by cloning into `~/.config/opencode/skills/`.

## Available Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| **study-programming** | Interactive programming tutor with spaced repetition, Socratic exercises, and progress tracking | `"teach me Python"`, `"I want to learn React"` |
| **convert-to-mind-map** | Converts Markdown notes into interactive Obsidian Markmind visual maps | `"convert this folder to a mind map"` |
| **youtube-summarizer** | Fetches a YouTube transcript (free, no API key) and produces a rich Obsidian note with structured sections, callouts, wikilinks, and actionable takeaways | `"لخصلي الفيديو ده"`, `"summarize this youtube video"` |

### study-programming

A full learning system that takes a learner from absolute zero to professional-level mastery of any programming language, framework, or tech topic.

**Features:**
- 3-level structured roadmap (Beginner -> Intermediate -> Advanced)
- Lesson-by-lesson teaching in Egyptian Arabic mixed with English technical terms
- Mandatory exercises after every lesson with Socratic hinting
- Confidence scoring, misconception logging, and progress tracking
- Spaced-repetition reviews at the start of every session
- Level capstone projects combining all taught concepts
- References section with real sources at the end of every lesson

### convert-to-mind-map

Reads existing Markdown notes from any folder and produces ready-to-open [Markmind](https://github.com/MarkMindCkm/obsidian-markmind)-compatible mind map files for Obsidian.

**Features:**
- Reads one or more Markdown files from a user-specified folder
- Analyzes content structure and groups related ideas into a clean hierarchy
- Produces `.md` files with `mindmap-plugin: basic` frontmatter
- Human-readable, bidirectional, zero manual work

### youtube-summarizer

Turns any YouTube video into a beautifully structured Obsidian note using only free tools — no API key, no signup.

**Features:**
- Fetches transcript automatically via `youtube-transcript-api` (supports manual and auto-generated captions)
- Fetches video metadata (title, channel, duration) via `yt-dlp`
- Interactive: asks for URL, save location, summary language, summary style, and emoji preference
- 4 summary styles: Quick Brief, Deep Dive, Study Notes, Action Plan
- 4 language options: English, فصيح, عامي مصري, Bilingual
- Pure Markdown + Obsidian features: callouts, wikilinks, highlights, checkboxes, frontmatter
- Caches transcripts locally to avoid redundant fetches
- Zero HTML — fully Obsidian-native output



```bash
cd ~/.config/opencode/skills/
git clone https://github.com/nagdista-dev/opencode-skills.git
```

Or copy any skill folder manually into `~/.config/opencode/skills/`.

## Requirements

- [OpenCode](https://opencode.ai) CLI installed
- (Optional) [Obsidian](https://obsidian.md) with the [Markmind](https://github.com/MarkMindCkm/obsidian-markmind) plugin for mind map features

## Contributing

Contributions are welcome. Open an issue or submit a pull request with a new skill or improvements to existing ones.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
