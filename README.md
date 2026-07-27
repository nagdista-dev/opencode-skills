# OpenCode Skills

A collection of custom [OpenCode](https://opencode.ai) skills that extend the AI assistant with specialized workflows. Drop these into your `~/.config/opencode/skills/` directory to install.

## Skills

### study-programming

Interactive programming tutor that builds a full learning system inside Obsidian. Teaches any programming language, framework, or tech topic from absolute zero to professional-level mastery.

**What it does:**
- Generates a structured 3-level roadmap (beginner / intermediate / advanced)
- Teaches lesson-by-lesson in Egyptian Arabic mixed with English technical terms
- Creates mandatory exercises after each lesson with Socratic hinting
- Tracks progress, confidence scores, and misconceptions in a single source-of-truth file
- Runs spaced-repetition reviews at the start of every session
- Builds level capstone projects that combine everything taught

**Key principles:**
- Zero-assumption teaching — every concept is explained as if the learner has never seen it before
- No lesson proceeds until the previous exercise is passed
- Technical terms are never translated — always kept in English
- All code blocks are 100% English

---

### convert-to-mind-map

Converts existing Markdown notes into interactive [Markmind](https://github.com/MarkMindCkm/obsidian-markmind)-compatible mind maps inside Obsidian.

**What it does:**
- Reads one or more Markdown files from a user-specified folder
- Analyzes content structure and groups related ideas
- Produces ready-to-open `.md` files with `mindmap-plugin: basic` frontmatter
- Creates clean, human-readable, bidirectional mind maps with zero manual work

---

## Installation

```bash
cd ~/.config/opencode/skills/
git clone https://github.com/nagdista/skills.git
```

Or manually copy the skill folder you want into `~/.config/opencode/skills/`.

## License

MIT
