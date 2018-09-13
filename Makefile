SHELL := /bin/bash
PACKAGE_NAME=demo-package.zip
PACKAGE_DIR=.package
.DEFAULT_GOAL := environment

environment:
	docker-compose build python

shell:
	docker-compose run --rm python bash

root:
	docker-compsose run --rm -u root python bash

.PHONY: tests
tests:
	docker-compose run --rm python make tests-actual

tests-actual:
	pytest --cov-report term-missing --cov=sippycup tests/

demo-package:
	rm -f $(PACKAGE_NAME)
	mkdir -p $(PACKAGE_DIR)
	cp -r sippycup lambda_function.py $(PACKAGE_DIR)
	pip3 install -t $(PACKAGE_DIR) flask
	cd $(PACKAGE_DIR) && zip -r ../$(PACKAGE_NAME) *

list-demo-package:
	unzip -l $(PACKAGE_NAME)

clean:
	rm -rf $(PACKAGE_NAME) $(PACKAGE_DIR) *.egg-info dist MANIFEST .cache .tox

pip-package:
	python setup.py sdist

pip-release: pip-package
	twine upload dist/*
