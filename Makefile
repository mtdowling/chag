tag:
	./chag tag --sign --debug CHANGELOG.rst

test:
	bats test/

deploy: tag
	git push origin --tags

.PHONY: test
