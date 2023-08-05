.PHONY: clean distclean
clean:
	find . -name '*.py[co]' -o -name '*.so' -o -name '__pycache__' -exec rm -rf \{} \;
distclean: clean
	rm -rf .coverage build/ dist/ *.egg-info/
build: distclean
	python setup.py check -mrs
	python setup.py build sdist bdist_wheel
	twine check dist/*
upload: build
	twine upload -s dist/*
