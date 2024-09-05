DC = docker compose


run:
	$(DC) up -d

build:
	$(DC) up --build

migrate:
	$(DC) exec web ./manage.py migrate

makemigrations:
	$(DC) exec web ./manage.py makemigrations
	make chown

test:
	$(DC) exec web ./manage.py test --noinput