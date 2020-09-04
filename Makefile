#!make

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Test transform function.
	@pipenv run pytest -v transform.py

run: ## Transform generated JSON file and create output files.
	@pipenv run python transform.py generated.json output

cleanup: ## Delete output files.
	@rm -v output_*.json
