.PHONY: activate
activate:
	pipenv shell

.PHONY: test
test: app-test

.PHONY: app-test
app-test:
	make start_local_dynamo
	pipenv run pytest || true
	make stop_local_dynamo

.PHONY: deploy
deploy:
	pipenv run sls deploy

.PHONY: deploy-function
deploy-function:
	pipenv run sls deploy function -f app

# ---------------- Local Dynamo ----------------
.PHONY: start_local_dynamo
start_local_dynamo:
	pipenv run ./scripts/start_local_dynamo.sh

.PHONY: stop_local_dynamo
stop_local_dynamo:
	pipenv run ./scripts/stop_local_dynamo.sh
