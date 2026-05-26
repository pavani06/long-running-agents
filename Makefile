SHELL := /bin/bash

.PHONY: lint lint-fix test-unit test-integration

lint:
	npm run lint

lint-fix:
	npm run lint:fix

test-unit:
	npm run test:unit -- $(ARGS)

test-integration:
	npm run test:integration -- $(ARGS)
