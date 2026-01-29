.PHONY: install test lint format run docker-build security-scan

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check .
	black --check .

format:
	black .
	ruff check . --fix

security-scan:
	bandit -r src/

run:
	uvicorn main:app --app-dir src --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t devops-service:latest .
