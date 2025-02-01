ONESHELL:

.PHONY: env
env:
	@find . -name ".env.example" | while read file; do \
		cp "$$file" "$$(dirname $$file)/.env"; \
	done


.PHONY: sync
sync:
	@uv sync --all-groups

.PHONY: setup
setup:
	@curl -LsSf https://astral.sh/uv/install.sh | sh


.PHONY: install_hooks
install_hooks:
	@pre-commit install

.PHONY: upd_hooks
upd_hooks:
	@pre-commit clean
	@pre-commit install --install-hooks

.PHONY: check
check:
	@git add .
	@pre-commit run

.PHONY: check-all
check-all:
	@git add .
	@pre-commit run --all

.PHONY: up
up: env setup sync

.PHONY: run
run: sync env
	@python -m src.main

.PHONY: test
test:
	pytest --maxfail=10 --disable-warnings --tb=short


.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: migrate-test
migrate-test: migrate test
