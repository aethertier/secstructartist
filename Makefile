PACKAGE_NAME = secstructartist

.PHONY: build install uninstall publish clean

build:
	pip install --upgrade pip build
	python -m build

install:
	pip install --upgrade pip setuptools
	pip install -e .

uninstall:
	pip uninstall -y $(PACKAGE_NAME)

publish:
	twine upload dist/*

clean:
	rm -rf dist $(PACKAGE_NAME).egg-info