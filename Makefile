@phony: up down shell-mongo shell dump-init test-integration test

help: ## show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: ## Rebuild the image locally to "backend"
	@docker build ./code/ --tag backend

halt: ## stop containers
	@docker-compose down --remove-orphans

up: ## run containers
	@docker-compose up -d

up-frontend: ## This will run npm locally on port 3000
	@cd frontend/dip && npm start

shell: ## Enter the backend container python
	@docker exec -it backend bash

test: test-integration

test-integration: ## This will run tests in docker, rebuild image if new or missing
	@docker-compose exec web pytest --capture=tee-sys tests/integration/tests.py

restart: halt up## This will reload containers

dump-init: ## This will dump database schema and save the new initdb.sql
	@docker exec postgres pg_dump --username=admin_dip --no-password --dbname=dipdb > ./database/init.sql

clean-images: ## This will clean all unused docker images not used by current containes
	@docker image prune -a --force

scan: ## With this you can scan an onion site, (eg. onion_site=fakeonion.onion) and get a json report to scan_result.log file
	@docker-compose exec lookup onionscan --jsonReport --verbose --torProxyAddress=0.0.0.0:9050 $(onion_site) > scan_result.log