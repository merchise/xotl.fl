RYE_EXEC ?= rye run
PYTHON_VERSION ?= 3.12
CARGO_HOME ?= $(HOME)/.cargo
PATH := $(HOME)/.rye/shims:$(CARGO_HOME)/bin:$(PATH)

SHELL := /bin/bash

PYTHON_FILES := $(shell find src/ -name '*.py')
RST_FILES := $(shell find docs/ -name '*.rst' -o -name 'conf.py')
THEME_FILES := $(shell find docs/source/_static -type f)

PYTEST_PATHS ?= "src/"
HYPOTHESIS_PROFILE ?= dev
PYTEST_HYPOTHESIS_ARGS ?=
PYTEST_EXTRA_ARGS ?=
PYTEST_FAILURE_ARGS ?= --ff --maxfail 1
PYTEST_ARGS ?= -vv $(PYTEST_FAILURE_ARGS) $(PYTEST_EXTRA_ARGS) $(PYTEST_HYPOTHESIS_ARGS)

USE_UV ?= true
REQUIRED_UV_VERSION ?= 0.2.2
REQUIRED_RYE_VERSION ?= 0.34.0
bootstrap:
	@INSTALLED_UV_VERSION=$$(uv --version 2>/dev/null | awk '{print $$2}' || echo "0.0.0"); \
    UV_VERSION=$$(printf '%s\n' "$(REQUIRED_UV_VERSION)" "$$INSTALLED_UV_VERSION" | sort -V | head -n1); \
	if [ "$$UV_VERSION" != "$(REQUIRED_UV_VERSION)" ]; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@INSTALLED_RYE_VERSION=$$(rye --version 2>/dev/null | head -n1 | awk '{print $$2}' || echo "0.0.0"); \
	DETECTED_RYE_VERSION=$$(printf '%s\n' "$(REQUIRED_RYE_VERSION)" "$$INSTALLED_RYE_VERSION" | sort -V | head -n1); \
	if [ "$$DETECTED_RYE_VERSION" != "$(REQUIRED_RYE_VERSION)" ]; then \
		rye self update || curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" RYE_VERSION="$(REQUIRED_RY_VERSION)" bash; \
	fi
	@rye config --set-bool behavior.use-uv=$(USE_UV)
	@rye pin --relaxed $(PYTHON_VERSION)

install: bootstrap
	@rye sync -f
	@cp requirements-dev.lock requirements-dev-py$$(echo $(PYTHON_VERSION) | sed "s/\.//").lock
.PHONY: install

sync: bootstrap
	@rye sync --no-lock
.PHONY: sync

lock: bootstrap
	@rye sync
	@cp requirements-dev.lock requirements-dev-py$$(echo $(PYTHON_VERSION) | sed "s/\.//").lock
.PHONY: lock


test: $(PYTHON_FILES)
	@rm -f .coverage*
	@pytest_workers_args=""; \
    if [ -n "$(PYTEST_WORKERS)" ]; then \
       pytest_workers_args="-n $(PYTEST_WORKERS)"; \
       if [ -n "$(PYTEST_MAXWORKERS)" ]; then \
          pytest_workers_args="$$pytest_workers_args --maxprocesses=$(PYTEST_MAXWORKERS)"; \
       fi \
    fi; \
    $(RYE_EXEC) pytest --cov-report= --cov-config=pyproject.toml --cov=src/ $$pytest_workers_args $(PYTEST_ARGS) $(PYTEST_PATHS);
.PHONY: test


docs/build: $(PYTHON_FILES) $(RST_FILES) $(THEME_FILES)
	@bash -c 'source .venv/bin/activate; make -C docs html'
	@touch docs/build

CADDY_SERVER_PORT ?= 9999
caddy: docs/build
	@docker run --rm -p $(CADDY_SERVER_PORT):$(CADDY_SERVER_PORT) \
         -v $(PWD)/docs/build/html:/var/www -it caddy \
         caddy file-server --browse --listen :$(CADDY_SERVER_PORT) --root /var/www
.PHONY: caddy

mypy:
	@$(RYE_EXEC) tox -e system-staticcheck
.PHONY: mypy

format:
	@$(RYE_EXEC) ruff check --fix src/
	@$(RYE_EXEC) isort src/
	@$(RYE_EXEC) ruff format src/
.PHONY: format

lint:
	@$(RYE_EXEC) ruff check src/
	@$(RYE_EXEC) ruff format --check src/
	@$(RYE_EXEC) isort --check src/
.PHONY: lint


shell:
	@$(RYE_EXEC) ipython
.PHONY: shell
