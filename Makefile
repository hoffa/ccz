all:
	flake8 --ignore E501 cx.py
	mypy --strict cx.py
