coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pyflunearyou tests
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run flake8 pyflunearyou
	pipenv run pydocstyle pyflunearyou
	pipenv run pylint pyflunearyou
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg pyflunearyou.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports pyflunearyou
