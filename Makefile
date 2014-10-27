test:
	bats test/

deploy:
	chag tag
	git push origin master
	git push origin --tags

.PHONY: test
