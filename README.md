# learn-any-thing

> A community collection of AI agent skills and workflows for developers. Currently featuring **`study-programming`** — an interactive, Egyptian-Arabic learning system that turns any programming topic into a full Obsidian-based course with a roadmap, lesson-by-lesson teaching, mandatory exercises, Socratic hints, and spaced-repetition review.

---

## Table of Contents

- [What is this?](#what-is-this)
- [Featured skill — `study-programming`](#featured-skill--study-programming)
  - [Why it is different from "explain and move on"](#why-it-is-different-from-explain-and-move-on)
  - [How it works](#how-it-works)
  - [The vault it builds](#the-vault-it-builds)
  - [Obsidian features it uses](#obsidian-features-it-uses)
  - [Language & cultural conventions](#language--cultural-conventions)
- [Install / Use the skill](#install--use-the-skill)
- [Repository structure](#repository-structure)
- [Contributing](#contributing)
- [License](#license)

---

## What is this?

This repository is a shared library of **AI agent skills** — reusable, agent-readable instructions (one `SKILL.md` per skill) that teach an AI assistant *how* to perform a specific workflow well.

Each skill lives in its own folder and follows a simple contract:

- A `SKILL.md` file with YAML frontmatter (`name`, `description`) that tells the agent **when** to activate the skill.
- A `references/` folder (optional) with templates, cheat sheets, and reference material the skill can pull in on demand.

Skills here are designed for coding-capable assistants (Claude, ZCode, Cursor, etc.) that support the skill format, and they are written to be **copied into an agent's skill directory and used as-is**.

---

## Featured skill — `study-programming`

`study-programming` is not a flashcard deck and not a static tutorial generator. It is a **complete learning system** that an AI tutor follows to teach you any programming or tech topic interactively, in **Egyptian Arabic (عامية مصرية)** mixed naturally with English technical terms.

It builds a full course for the topic you name — *React, Python, Docker, Git, JavaScript, SQL, anything* — as a set of **Obsidian-compatible Markdown files** that you keep and own.

### Why it is different from "explain and move on"

Most AI answers explain a concept once and move on. This skill is built on four deliberate principles:

| Principle | What it actually means |
| --- | --- |
| **Never skips ahead** | The learner must pass the exercise for lesson *N* before lesson *N+1* even exists. |
| **Teaches Socratically** | When the learner struggles, the skill guides *toward* the answer with hints and counterexamples — it never hands the solution over. |
| **Stops on purpose** | After a lesson and its recap, the tutor stops explicitly and waits. It never lectures and then keeps talking. |
| **Fights forgetting** | Uses **spaced repetition** of past lessons (1d → 3d → 7d → 14d → 30d) at the start of every session, not just forward progress. |

It also **web-searches the topic first** to lock in current best practices, stable versions, and common beginner misconceptions — rather than trusting stale model knowledge.

### How it works

The skill follows a strict 6-step workflow on top of a permanent `progress.md` file that is the **single source of truth** for where you are.

```
Step 0  Pick topic + save location + resume check (if a progress.md exists)
Step 1  Research current best practices / versions / misconceptions (web search)
Step 2  Build the full 3-level roadmap up front (beginner / intermediate / advanced)
Step 3  Teach the current lesson only, then stop and wait
Step 4  Exercise + evaluation: pass → advance; fail → Socratic hints + retry
Step 5  Spaced repetition review at the start of every session
```

The evaluation loop is what makes it a *course* rather than a *chat*:

- **Correct answer** → mark the lesson complete, schedule its spaced-repetition review, then ask if you are ready for the next lesson (it never auto-advances).
- **Incorrect answer** → run a Socratic sequence: restate what your code does → justify a specific choice → test it against a counterexample → if still stuck, point at the exact concept to revisit. Log the misconception. Let you retry the *same* exercise. The full solution is never revealed.

### The vault it builds

For a topic like `react`, the skill creates this structure at your chosen save location (default `~/Documents/<topic-slug>/`):

```
react/
├── roadmap.md              # full 3-level roadmap, built once up front
├── progress.md             # source of truth: current position, completed lessons,
│                            # spaced-repetition review schedule, misconceptions log
├── lessons/
│   ├── 01-<slug>.md
│   ├── 02-<slug>.md
│   └── ...
└── exercises/
    ├── 01-<slug>-exercise.md
    ├── 02-<slug>-exercise.md
    └── ...
```

Each lesson file has its own frontmatter (`lesson`, `topic`, `level`, `status`, `tags`, `aliases`, plus `roadmap:` and `exercise:` wikilinks), a concept explanation, an example block, an optional Mermaid diagram, a recap, and a wikilink into its exercise. Each exercise file tracks `attempts` and `status`. `progress.md` tracks completed lessons, the spaced-repetition schedule, and a misconceptions log you build up over time.

The exact file templates are documented in [`study-programming/references/templates.md`](study-programming/references/templates.md) — the skill copies them verbatim so the vault stays internally consistent.

### Obsidian features it uses

Because the output is meant to live in an Obsidian vault, the skill uses Obsidian's Markdown extensions where they genuinely help — never as decoration:

- **Wikilinks** (`[[file]]`, `[[file|display]]`) for every cross-reference between roadmap ↔ lessons ↔ exercises ↔ progress.
- **Callouts** (`> [!note]`, `> [!tip]`, `> [!warning]`, `> [!question]`) for side-notes, common-mistake warnings, and Socratic hint prompts.
- **Frontmatter tags** (`#beginner`, `#intermediate`, `#advanced`, `#<topic-slug>`) so the vault's tag pane can filter lessons by level.
- **Task lists** (`- [ ]` / `- [x]`) so progress is visibly checkable inside Obsidian, not just in `progress.md`.
- **Block references** (`^block-id` + `[[file#^block-id]]`) when a later lesson or a review question needs to point at an exact line.
- **Mermaid diagrams** for inherently structural concepts (event loop, request/response, Git branch model, component trees).
- **Footnotes** and **frontmatter aliases** for optional deeper dives and search.

### Language & cultural conventions

The skill is opinionated about language because it is built for Egyptian/Arab learners specifically:

- **Prose is Egyptian Arabic mixed with English technical terms** — the way Egyptian developers actually talk (`"دلوقتي هنعمل loop على الـ array دي وهنستخدم map function"`). Technical terms are kept in English, never forcibly translated.
- **Code is 100% English, no exceptions.** Every code block — names, comments, string literals, sample output — is fully English. Zero Arabic-script characters are allowed inside any code fence.
- **RTL flow protection.** No line or heading may *start* with a bare English word, because that breaks Arabic's right-to-left reading direction; English technical terms are prefixed with `الـ` when they lead a line.
- **Culturally natural examples** for an Egyptian/Arab/Muslim learner — no alcohol, dating, or gambling themes — without forcing religious references where they are irrelevant.
- **No emojis anywhere** — plain text and Markdown formatting only.

---

## Install / Use the skill

1. **Install** by copying the `study-programming/` folder into your agent's skill directory:

   ```
   <agent-skills-dir>/study-programming/
   ├── SKILL.md
   └── references/templates.md
   ```

   For example, with ZCode/Claude-style agents this is typically `~/.agents/skills/` or `~/.zcode/skills/`. The skill's `description` frontmatter is what tells the agent to activate it automatically.

2. **Trigger it** by asking to learn any topic in any language. Any of these will fire it:

   - "عايز أتعلم React"
   - "علمني Python"
   - "I want to learn Docker"
   - "ابنيلي كورس كامل في Git"
   - "كمل معايا في اللي كنا بندرسه" *(resume)*

3. **Pick a save location** when the agent asks (default is your `Documents` folder), then open that folder as an Obsidian vault to navigate the roadmap, lessons, and progress as you go.

> Resuming works automatically: if a `progress.md` already exists at the save location, the skill reads it first and continues exactly from where you left off — including due spaced-repetition reviews.

---

## Repository structure

```
.
└── study-programming/
    ├── SKILL.md                      # the skill instructions (when + how)
    └── references/
        └── templates.md              # exact Markdown/frontmatter templates for every file
```

---

## Contributing

New skills and improvements to existing ones are welcome. To add a skill:

1. Create a `<skill-name>/` folder at the repository root.
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) describing **when** the skill should activate — the `description` is what an agent matches against, so make it concrete and trigger-rich.
3. Put any reference material the skill loads on demand into `<skill-name>/references/`.
4. Open a pull request against `main`.

Please keep each skill self-contained (no cross-skill dependencies unless documented) and follow the existing folder + frontmatter convention.

---

## License

This repository is shared with the community. Add a `LICENSE` file if you need a specific license for your project; otherwise, contributions here are intended for open community use.
