# Contributing

This is a one-person learning project, and corrections are welcome. The goal of the repo is that a complete beginner can follow it
without having to ask anyone, so **any place you got stuck is a bug**.

## The most useful things you can send

- **"I did not understand X."** Open an issue naming the page and the word or step. If it is missing from the [glossary](docs/glossary.md), that is the fix.
- **A wrong fact.** A part that is out of stock or discontinued, a datasheet that says something different, a wiring error. Say where you found the right answer.
- **A better explanation.** A shorter sentence, a clearer picture.

## Rules of thumb

- Keep US-only sourcing (see `CLAUDE.md`), and say whether a price came from an API or a web page.
- Do not hand-edit a **generated** file. Edit the data (`pinmap.json`, `parts-shortlist.json`, `amazon-items.json`) and run `make`. `make check` should pass before you push.
- Start every document with the four-line header described in [docs/README.md](docs/README.md), and use the same status words (*Planned*, *Seller claim*, *Measured*, *Tested*).
- Do not commit credentials. `.env` is git-ignored: keep it that way.
- Explain a new term the first time you use it, or add it to the glossary.
