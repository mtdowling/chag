test:
	bats test/

deploy: tag
	git push origin master
	git push origin --tags

.PHONY: test
