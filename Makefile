tag:
	./chag tag --sign --debug CHANGELOG.rst latest

test:
	bats test/

deploy: tag
	git push origin --tags

.PHONY: test
