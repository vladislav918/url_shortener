DC = docker compose
LOGS = docker logs

run:
	$(DC) up -d

build:
	$(DC) up --build -d

down:
	$(DC) down	

migrate:
	$(DC) exec web ./manage.py migrate

makemigrations:
	$(DC) exec web ./manage.py makemigrations

logs:
	$(LOGS) web -f

test:
	$(DC) exec web ./manage.py test --noinput

superuser:
	$(DC) exec web python manage.py createsuperuser