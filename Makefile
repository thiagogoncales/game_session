.PHONY: activate
activate:
	pipenv shell

.PHONY: test
test: app-test

.PHONY: app-test
app-test:
	make stop_local_dynamo
	make start_local_dynamo
	pipenv run pytest || true
	make stop_local_dynamo

.PHONY: deploy
deploy:
	pipenv run sls deploy

.PHONY: deploy-function
deploy-function:
	pipenv run sls deploy function -f app

.PHONY: start
start:
	pipenv run sls wsgi serve

# ---------------- Local Dynamo ----------------
.PHONY: start_local_dynamo
start_local_dynamo:
	pipenv run ./scripts/start_local_dynamo.sh

.PHONY: stop_local_dynamo
stop_local_dynamo:
	pipenv run ./scripts/stop_local_dynamo.sh
