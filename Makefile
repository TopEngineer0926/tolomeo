@phony: up down shell-mongo shell dump-init test-integration test

help: ## show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

up: ## run containers
	@docker-compose up -d

build: ## Rebuild the image locally to "backend"
	@docker build ./code/ --tag backend

halt: ## stop containers
	@docker-compose down --remove-orphans

# tutorials for mongo can be found here https://docs.mongodb.com/manual/mongo/
shell-mongo: ## Enter the mongodb container, access to mongodb with 'mongo -u root -p secret'
	@docker exec -it mongodb bash

shell: ## Enter the backend container python
	@docker exec -it backend bash

test: test-integration

test-integration: ## This will run tests in docker, rebuild image if new or missing
	@docker-compose exec web pytest --capture=tee-sys tests/integration/tests.py

restart: ## This will reload containers
	@docker-compose pull && docker-compose restart

dump-init: ## This will dump database schema and save the new initdb.sql
	@docker exec postgres pg_dump --username=admin_dip --no-password --dbname=dipdb > ./database/init.sql