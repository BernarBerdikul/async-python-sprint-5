start:  # Building Docker images and start
	docker compose -f docker-compose.yml up -d --build

test:  # Start Docker test containers
	docker compose -f docker-compose.test.yml up -d --build

migrate:  # Run migrations
	alembic upgrade head

localtest:  # start pytest
	pytest -vv

pre-commit:  # Run pre-commit
	pre-commit run --all-files
