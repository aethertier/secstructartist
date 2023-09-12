PACKAGE_NAME = secstructartist

.PHONY: build install uninstall publish clean

build:
	python3 setup.py sdist bdist_wheel

install:
	pip install dist/$(PACKAGE_NAME)-*.tar.gz

uninstall:
	-pip uninstall -y $(PACKAGE_NAME)

publish:
	twine upload dist/*

clean:
	rm -rf dist build $(PACKAGE_NAME).egg-info