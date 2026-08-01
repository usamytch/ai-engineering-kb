PYTHON ?= python3

.PHONY: check inbox

check:
	$(PYTHON) scripts/check_kb.py

inbox:
	$(PYTHON) scripts/refresh_inbox.py

