# One command to rebuild everything generated in this repo. See docs/getting-started.md.
PY ?= python3

.PHONY: all wiring parts site test check help

all: wiring parts site   ## regenerate wiring docs, pins.h, parts.md and the site images

wiring:                  ## pinmap.json -> wiring docs, diagrams, docs/pinout.html, firmware/ksp/include/pins.h
	$(PY) tools/gen_wiring.py

parts:                   ## parts-shortlist.json + amazon-items.json -> hardware/sourcing/parts.md (offline)
	$(PY) tools/parts.py budget --md

site:                    ## copy the renders that the GitHub Pages landing page shows
	mkdir -p docs/img
	cp hardware/mockup/renders/iso.png hardware/mockup/renders/seat-view.png docs/img/

test:                    ## offline tests, no network or keys needed
	cd tools && $(PY) -B -m unittest

check:                   ## fail if a committed generated file is out of date
	$(PY) tools/check_generated.py

help:                    ## list the targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/ -/'
