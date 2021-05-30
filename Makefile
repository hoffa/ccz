all:
	python3 -m venv .venv
	.venv/bin/python -m pip install black flake8 mypy
	.venv/bin/black .
	.venv/bin/flake8 --ignore E501 cx
	.venv/bin/mypy --strict cx