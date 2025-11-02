.PHONY: install lint test run docker-up docker-down

install:
	python -m pip install -r requirements.txt

lint:
	python -m flake8 backend scripts

test:
	pytest backend/tests

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
