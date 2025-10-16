COMPOSE = docker-compose -f docker-compose.yml

all: up

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down --rmi all --volumes

re: down up