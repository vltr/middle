SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = middle
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "clean - let this project be near mint"
	@echo "test - run tests with coverage"
	@echo "release - package and upload a release"

.PHONY: help Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

black:
	black ./src/middle/ ./tests setup.py

cleanpycache:
	find . -type d | grep "__pycache__" | xargs rm -rf

clean: cleanpycache
	rm -rf ./.coverage
	rm -rf ./.pytest_cache
	rm -rf ./.tox
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./htmlcov
	rm -rf ./src/*.egg-info

requirements-dev:
	pip install pip-tools
	pip-compile requirements-dev.in --output-file requirements-dev.txt
	pip-compile
	pip-sync requirements-dev.txt requirements.txt

release:
	tox -e check
	python setup.py clean --all sdist bdist_wheel
	twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip
