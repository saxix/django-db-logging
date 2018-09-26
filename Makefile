BUILDDIR='~build'


.mkbuilddir:
	mkdir -p ${BUILDDIR}

develop:
	$(MAKE) requirements
	@pipenv install -d
	@pipenv install -e .[test]


requirements:
	pipenv lock --requirements -d > src/requirements/testing.pip
	pipenv lock --requirements > src/requirements/install.pip

test:
	pipenv run py.test -v --create-db

lint:
	pipenv pre-commit --all-files


clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage coverage.xml .eggs .pytest_cache
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find tests -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf

fullclean:
	rm -fr .tox .cache .venv .pytest_cache src/django_db_logger.egg-info
	$(MAKE) clean


docs: .mkbuilddir
	mkdir -p ${BUILDDIR}/docs
	sphinx-build -aE docs/ ${BUILDDIR}/docs
ifdef BROWSE
	firefox ${BUILDDIR}/docs/index.html
endif
