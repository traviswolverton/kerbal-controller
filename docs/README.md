# Docs

> **What this covers:** a map of the documents, the status words used across the repo, and the header every document starts with.  
> **Read it if:** you are lost, or you are adding a document.  
> **Status:** Reference.  
> **Next:** [How it works](how-it-works.md).

## Map

| Document | Answers |
|---|---|
| [how-it-works.md](how-it-works.md) | What is this and how does it fit together? |
| [glossary.md](glossary.md) | What does this word mean? |
| [journey.md](journey.md) | How did the project get here, and what went wrong? |
| [design/decisions.md](design/decisions.md) | What was chosen, why, and what is still open? |
| [design/why-not.md](design/why-not.md) | Why not the other way? |
| [design/controls.md](design/controls.md) | What does each control do in the game? |
| [design/todo.md](design/todo.md) | What is left, and what blocks what? |
| [firmware/architecture.md](firmware/architecture.md) | How will the firmware be organised? |
| [getting-started.md](getting-started.md) | How do I run or rebuild things? |
| [gallery.md](gallery.md) | What does it look like? |
| [pinout.html](pinout.html) | The wiring diagrams as a web page (generated) |

Outside `docs/`: [parts and budget](../hardware/sourcing/parts.md), [CAD](../hardware/cad/README.md), [mockup](../hardware/mockup/README.md), [wiring](../hardware/electronics/wiring/wiring.md),
[electronics build](../hardware/electronics/electronics-build.md), [first power-up](../hardware/electronics/bring-up.md), [firmware](../firmware/README.md) and [tools](../tools/README.md).

## Status words

Every document says what state it is in, and a quoted number is only as good as its status. Use the same words everywhere.

**For a stage of work** (the board in the [README](../README.md)):

| Word | Meaning |
|---|---|
| **Not started** | Nothing exists yet |
| **In progress** | Some of it exists, and it is not finished |
| **Done** | Finished and checked |

**For a fact** (a size, a rating, a pin, a behaviour), from least to most trustworthy:

| Word | Meaning | Example |
|---|---|---|
| **Planned** | Decided on paper. Nothing checked | "Pot supplied from 3V3" |
| **Seller claim** | Read from a listing or datasheet. Not checked on the real part | "Fader face is 146.5 mm long" |
| **Measured** | Checked with calipers or a meter on the real part | "Hole spacing is 62 mm" |
| **Tested** | Worked on the bench or in the game | "Throttle follows KSP" |

At the time of writing, nothing about the hardware is **Measured** or **Tested**: the parts have not arrived. When one becomes so, change its
word and say when, for example "Measured 2026-11-03". The [to-do](design/todo.md) is mostly the list of facts waiting to be promoted.

## The header

Every hand-written document starts with a four-line block so a reader can tell at once whether to read it:

```markdown
# Title

> **What this covers:** one sentence.  
> **Read it if:** who it is for, or what question it answers.  
> **Status:** Planned | Seller claim | Measured | Tested | Reference (plus a clause if useful).  
> **Next:** the document to read after this one.
```

End the first three lines with two spaces so Markdown shows them on separate lines. Generated files carry the same block, written by the script that makes them. To change one, change the script.

## Generated files

Marked **generated** at the top. Edit the data, not the output, then run `make` (see [getting started](getting-started.md)):

| File | Made by | From |
|---|---|---|
| `docs/pinout.html`, `hardware/electronics/wiring/wiring.md`, `pin-map.md`, `diagrams/*.svg`, `firmware/ksp/include/pins.h` | `tools/gen_wiring.py` | `hardware/electronics/pinmap.json` |
| `hardware/sourcing/parts.md` | `tools/parts.py budget --md` | `parts-shortlist.json`, `amazon-items.json` |
| `docs/img/*.png` | `make site` | `hardware/mockup/renders/` |
