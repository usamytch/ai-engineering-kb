PYTHON ?= python3
TRIAGE_FILE ?=
TRIAGE_ARGS ?=
WEEK ?=
PROVIDER ?= codex
MODEL ?=
PROFILE ?= deep
PAPER ?=
REVIEWER ?=
AIDB_ARGS ?=

.PHONY: check inbox triage week-start week-status week-process review week-close paper paper-fetch paper-extract paper-summary paper-status paper-approve

check:
	$(PYTHON) scripts/check_kb.py
	$(PYTHON) -m unittest discover -s tests

inbox:
	$(MAKE) week-start

triage:
	$(PYTHON) scripts/triage_inbox.py $(if $(TRIAGE_FILE),--file "$(TRIAGE_FILE)",) $(TRIAGE_ARGS)

week-start:
	$(PYTHON) -m aidb week-start $(if $(WEEK),--week "$(WEEK)",) $(AIDB_ARGS)

week-status:
	$(PYTHON) -m aidb week-status $(if $(WEEK),--week "$(WEEK)",) $(AIDB_ARGS)

week-process:
	$(PYTHON) -m aidb week-process $(if $(WEEK),--week "$(WEEK)",) --provider "$(PROVIDER)" --profile "$(PROFILE)" $(if $(MODEL),--model "$(MODEL)",) $(AIDB_ARGS)

review:
	$(PYTHON) -m aidb review $(AIDB_ARGS)

week-close:
	$(PYTHON) -m aidb week-close $(if $(WEEK),--week "$(WEEK)",) $(AIDB_ARGS)

paper:
	@test -n "$(PAPER)" || (echo "Usage: make paper PAPER=2608.16889v1 [PROVIDER=codex]" >&2; exit 2)
	$(PYTHON) -m aidb paper process "$(PAPER)" --provider "$(PROVIDER)" --profile "$(PROFILE)" $(if $(MODEL),--model "$(MODEL)",) $(AIDB_ARGS)

paper-fetch:
	@test -n "$(PAPER)" || (echo "Usage: make paper-fetch PAPER=2608.16889v1" >&2; exit 2)
	$(PYTHON) -m aidb paper fetch "$(PAPER)" $(AIDB_ARGS)

paper-extract:
	@test -n "$(PAPER)" || (echo "Usage: make paper-extract PAPER=2608.16889v1" >&2; exit 2)
	$(PYTHON) -m aidb paper extract "$(PAPER)" $(AIDB_ARGS)

paper-summary:
	@test -n "$(PAPER)" || (echo "Usage: make paper-summary PAPER=2608.16889v1 [PROVIDER=codex]" >&2; exit 2)
	$(PYTHON) -m aidb paper summarize "$(PAPER)" --provider "$(PROVIDER)" --profile "$(PROFILE)" $(if $(MODEL),--model "$(MODEL)",) $(AIDB_ARGS)

paper-status:
	@test -n "$(PAPER)" || (echo "Usage: make paper-status PAPER=2608.16889v1" >&2; exit 2)
	$(PYTHON) -m aidb paper status "$(PAPER)"

paper-approve:
	@test -n "$(PAPER)" || (echo "Usage: make paper-approve PAPER=2608.16889v1 REVIEWER=name" >&2; exit 2)
	@test -n "$(REVIEWER)" || (echo "Usage: make paper-approve PAPER=2608.16889v1 REVIEWER=name" >&2; exit 2)
	$(PYTHON) -m aidb paper approve "$(PAPER)" --reviewer "$(REVIEWER)"
