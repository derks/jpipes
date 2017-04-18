.PHONY: all init clean

all: init clean

init:
	pip install --upgrade -r requirements.txt

clean:
	find . -name '*.py[co]' -delete
