
.PHONY: venv deps init run test ci

PY?=python

venv:
	$(PY) -m venv .venv

deps:
	pip install -r requirements.txt

init:
	$(PY) scripts/init_db.py

run:
	uvicorn app.main:app --host 127.0.0.1 --port 8000

test:
	pytest -q

ci:
	mkdir -p EVIDENCE/S08
	pytest --junitxml=EVIDENCE/S08/test-report.xml -q

ci-2:
	python3 -m venv .venv
	@if [ -d ".venv/bin" ]; then \
		VENV_BIN=".venv/bin"; \
	else \
		VENV_BIN=".venv\\Scripts"; \
	fi; \
	$$VENV_BIN/pip install -r requirements.txt; \
	$$VENV_BIN/python scripts/init_db.py; \
	mkdir -p EVIDENCE/S06; \
	$$VENV_BIN/pytest --junitxml=EVIDENCE/S06/test-report.xml -q