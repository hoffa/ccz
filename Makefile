all:
	flake8 --ignore E501 cx
	mypy --strict cx
