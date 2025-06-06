SHELL := /bin/bash

define execute_in_env
	export PYTHONPATH=./src:./layers/shared_utils/python && source venv/bin/activate && $1
endef

create-environment:
	@echo ">>> Setting up Venv"
	python3 -m venv venv

install-external-requirements: create-environment
	@echo ">>> Installing external requirements."
	$(call execute_in_env, pip install -r ./requirements/requirements-external.txt)

install-lambda-requirements: create-environment
	@echo ">>> Installing lambda requirements."
	$(call execute_in_env, pip install -r ./requirements/requirements-lambda.txt)

install-dev-tools: create-environment
	@echo ">>> Installing dev tools requirements"
	$(call execute_in_env, pip install -r ./requirements/requirements-dev-tools.txt)

run-python-checks: install-external-requirements install-lambda-requirements install-dev-tools
	@echo ">>> Running pytest"
	$(call execute_in_env, pytest --testdox -vvvrP --cov=src --cov-fail-under=90 test/*)
	@echo ">>> Running security checks"
	$(call execute_in_env, bandit -lll */*.py *c/*.py)
	@echo ">>> Running ruff"
	$(call execute_in_env, ruff check src)
	$(call execute_in_env, ruff check test)

prepare-external-requirements-zip: create-environment
	@echo ">>> Preparing the external requirements for packaging."
	$(call execute_in_env, pip install -r ./requirements/requirements-external.txt -t ./layers/externals/python)