coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=aioambient tests
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run flake8 aioambient
	pipenv run pydocstyle aioambient
	pipenv run pylint aioambient
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg aioambient.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports aioambient
