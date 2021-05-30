all:
	flake8 cx.py
	mypy --strict cx.py