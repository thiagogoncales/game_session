.PHONY: test
test:
	make start_local_dynamo
	pipenv run pytest
	make stop_local_dynamo

# ---------------- Local Dynamo ----------------
.PHONY: start_local_dynamo
start_local_dynamo:
	pipenv run ./scripts/start_local_dynamo.sh

.PHONY: stop_local_dynamo
stop_local_dynamo:
	pipenv run ./scripts/stop_local_dynamo.sh
