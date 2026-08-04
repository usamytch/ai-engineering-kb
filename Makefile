PYTHON ?= python3
TRIAGE_FILE ?=
TRIAGE_ARGS ?=

.PHONY: check inbox triage

check:
	$(PYTHON) scripts/check_kb.py
	$(PYTHON) -m unittest discover -s tests

inbox:
	$(PYTHON) scripts/refresh_inbox.py

triage:
	$(PYTHON) scripts/triage_inbox.py $(if $(TRIAGE_FILE),--file "$(TRIAGE_FILE)",) $(TRIAGE_ARGS)
