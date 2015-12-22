.PHONY: docs

setup:
	python setup.py install

init:
	pip install -r requirements.txt

test:
	sudo py.test tests --doctest-modules --pep8 etl2osm -v --cov etl2osm --cov-report term-missing

clean:
	python setup.py clean --all
	rm -rf build-*
	rm -rf *egg*
	rm -rf dist

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

register:
	python setup.py register
