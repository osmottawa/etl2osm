.PHONY: docs

setup:
	python setup.py install

init:
	pip install -r requirements.txt

test:
	py.test test_etl2osm.py --verbose

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
