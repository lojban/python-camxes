.PHONY: test

all: test

test:
	@python -mattest.run camxes.tests.all -rquickfix
