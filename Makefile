tag:
	./chag tag --sign --debug CHANGELOG.rst

test:
	bats test/

.PHONY: test
