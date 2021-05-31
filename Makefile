# Signifies our desired python version
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
.PHONY: install test

.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To test the project type make test"
	@echo "------------------------------------"

test:
	PYTHONPATH=./test ${PYTHON} -m pytest