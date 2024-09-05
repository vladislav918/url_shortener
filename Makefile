DC = docker compose


run:
	$(DC) up

build:
	$(DC) up --build

down:
	$(DC) down	

migrate:
	$(DC) exec web ./manage.py migrate

makemigrations:
	$(DC) exec web ./manage.py makemigrations
	make chown

test:
	$(DC) exec web ./manage.py test --noinput