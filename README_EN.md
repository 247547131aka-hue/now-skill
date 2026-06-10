# now.skill — Distill Your Current Partner into an AI Skill

> ⚡ **ex-skill is past tense. now-skill is present continuous.**

Turn your current partner (or anyone) into a runnable AI Skill. Import chats, photos, social media, and personal observations. Build a dual-layer memory + 5+1 layer persona model. Supports **risk rehearsal**, **daily conversation simulation**, and **relationship trend analysis** — with continuous incremental updates.

---

## 🔥 Key Differences from ex-skill

| Dimension | ex-skill | **now-skill** |
|-----------|----------|---------------|
| **Tense** | Past (frozen archive) | **Present continuous (living data)** |
| **Memory** | Single-layer frozen | **Dual-layer**: Frozen + Living |
| **Persona** | 5 static layers | 5 static + **Trending Signals layer** |
| **Updates** | Full rebuild | **Incremental delta** + auto snapshots |
| **Modes** | Chat + Recall | Chat + **Risk Rehearsal** + **Pulse Check** |
| **Data import** | Manual file paths | **Inbox drag-drop** + **paste feed** + screenshot |

---

## 🎯 Three Modes

### 💬 Chat Mode `/{slug}`
Talk to them. They respond in their voice, with their catchphrases and emotional patterns.

### ⚠️ Risk Rehearsal `/{slug}-risk`
Predict how they'd react to something you want to say or do. Three scenarios: best case, most likely, worst case — plus safe expression suggestions.

### 📊 Pulse Check `/{slug}-pulse`
Analyze recent interaction trends: emotional trajectory, topic shifts, potential risk signals.

---

## 🚀 Quick Start

### Install

**Method 1: Claude Code (recommended)**

```bash
git clone https://github.com/247547131aka-hue/now-skill ~/.claude/skills/now-skill
```

Update: `cd ~/.claude/skills/now-skill && git pull`

**Method 2: Project-level**

```bash
mkdir -p .claude/skills
git clone https://github.com/247547131aka-hue/now-skill .claude/skills/now-skill
```

**Method 3: Claude.ai (web)**

Skills mechanism not supported — copy SKILL.md content into conversation and follow instructions manually.

**Method 4: Other Agents (Cursor / Cline / Codex etc.)**

Skill/Plugin mechanisms vary by platform. Adapt `SKILL.md` + `prompts/` as reference.

### Create

In Claude Code:

```
/create-now
```

Answer 4 questions. Then:

```
/{slug}-risk I want to tell them I need more alone time, how should I say it?
```

---

## 📥 Frictionless Data Import

| Method | How | Best for |
|--------|-----|----------|
| **Inbox** 📥 | Drop files into `nows/{slug}/inbox/`, run `/now-update {slug}` | Bulk imports |
| **Paste Feed** 💬 | `/now-feed {slug}` then paste chat | Right after chatting |
| **Screenshots** 📸 | Drop screenshots into inbox | Mobile chats |
| **Traditional** 📂 | Same as ex-skill (WeChat/QQ/social/photos) | First-time big import |

---

## 🛠️ Commands

| Command | Function |
|---------|----------|
| `/create-now` | Create a new now-skill |
| `/{slug}` | Chat mode |
| `/{slug}-risk` | Risk rehearsal |
| `/{slug}-pulse` | Relationship pulse |
| `/now-update {slug}` | Scan inbox for updates |
| `/now-feed {slug}` | Paste chat feed |
| `/now-list` | List all now-skills |
| `/now-delete {slug}` | Delete |
| `/now-rollback {slug}` | Rollback |

---

## ⚠️ Safety

1. **For understanding and improving relationships only**
2. **All data stored locally** — never uploaded
3. **Does not replace real communication** — predictions are guesses
4. **Privacy protection** — no identifiable info exposed
5. **Not for manipulation** — don't use predictions to deceive

---

## 📄 License

MIT License

## 🙏 Acknowledgments

Inspired by [ex-skill](https://github.com/therealXiaomanChu/ex-skill), [colleague-skill](https://github.com/titanwings/colleague-skill), and [yourself-skill](https://github.com/notdog1998/yourself-skill).
