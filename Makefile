.PHONY: all init clean

all: init clean

init:
	pip install --upgrade -r requirements.txt

clean:
	find . -name '*.py[co]' -delete
	rm -rf build/* dist/*

release: clean
	python setup.py sdist
	python setup.py bdist_wheel

deploy: release
	twine upload dist/*

