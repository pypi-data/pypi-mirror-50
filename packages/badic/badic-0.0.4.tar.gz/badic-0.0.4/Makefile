PYTHON ?= python
PIP = $(PYTHON) -m pip -v

install: configure
	$(PIP) install --no-index --ignore-installed --no-deps .

clean:
	rm -rf build/
	rm -f $(find . -name *.so)
	rm -f $(find . -name *.pyc)
	rm -f configure config.log config.json

configure: configure.ac
	autoconf

sdist: configure
	$(PYTHON) setup.py sdist
