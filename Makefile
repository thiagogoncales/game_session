FLASK_APP=app/app.py

.PHONY: freeze_requirements
freeze_requirements:
	pip freeze > requirements.txt

.PHONY: start
start:
	FLASK_APP=${FLASK_APP} flask run

.PHONY: activate
activate:
	pipenv shell

.PHONY: test
test: app-tests

.PHONY: app-tests
app-tests:
	make -C app test
