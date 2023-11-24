# Adapted from https://github.com/Textualize/frogmouth/blob/main/Makefile
##############################################################################
# Common make values.
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
package     := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
# Replace "-" with "_" in the package name
package     := $(shell echo $(package) | tr - _)
run         := poetry run
python      := $(run) python
lint        := $(run) pylint
mypy        := $(run) mypy
black       := $(run) black
isort       := $(run) isort
bandit      := $(run) bandit
monkey      := $(run) monkeystype
pytest      := $(run) pytest
pyre        := $(run) pyre

DOCDIR      := docs
DOCSRC      := $(DOCDIR)/source
BUILDDIR    := $(DOCDIR)/build/html
SPHINXOPTS  :=


##############################################################################
# Methods of running the application.
.PHONY: run
run:				# Run the application
	$(python) -m $(package)

.PHONY: debug
debug:				# Run the application in debug mode
	TEXTUAL=devtools make run

##############################################################################
# Setup/update packages the system requires.
.PHONY: setup
setup:				# Set up the development environment
	poetry install
	$(run) pre-commit install

.PHONY: update
update:				# Update the development environment
	poetry update

##############################################################################
# Package building and distribution.
.PHONY: build
build:				# Build the package for distribution
	poetry build

.PHONY: clean
clean:				# Clean up the package builds
	rm -rf dist

##############################################################################
# Reformatting tools.
.PHONY: black
black:				# Run black over the code
	$(black) $(package)

.PHONY: isort
isort:				# Run isort over the code
	$(isort) $(package)

.PHONY: reformat
reformat: isort black		# Run all the formatting tools over the code

##############################################################################
# Documentation.
doc:                # Build the documentation
	sphinx-quickstart "$(DOCDIR)"

apidoc:             # Build the API documentation
	sphinx-apidoc -o "$(DOCSRC)" .

html:               # Build the HTML documentation
	sphinx-build "$(DOCSRC)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:           # Run a live-updating HTML server for the documentation
	sphinx-autobuild "$(DOCSRC)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

##############################################################################
# Checking/testing/linting/etc.
.PHONY: lint
lint:				# Run Pylint over the library
	$(lint) $(package)

.PHONY: typecheck
typecheck:			# Perform static type checks with mypy
	$(mypy) --scripts-are-modules $(package)

.PHONY: stricttypecheck
stricttypecheck:	# Perform strict static type checks with mypy
	$(mypy) --scripts-are-modules --strict $(package)

.PHONY: bandit
bandit:				# Run bandit over the code
	$(bandit) -r $(package)

.PHONY: monkey
monkey:				# Run monkeytype over the code
	$(monkey) apply $(package)

.PHONY: test
test:				# Run the unit tests
	$(pytest) tests

.PHONY: checkall
checkall: lint stricttypecheck bandit # Check all the things

##############################################################################
# Utility.
.PHONY: repl
repl:				# Start a Python REPL
	$(python)

.PHONY: shell
shell:				# Create a shell within the virtual environment
	poetry shell

.PHONY: help
help:				# Display this help
	@grep -Eh "^[a-z]+:.+# " $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.+# "}; {printf "%-20s %s\n", $$1, $$2}'

##############################################################################
# Housekeeping tasks.
.PHONY: housekeeping
housekeeping:		# Perform some git housekeeping
	git fsck
	git gc --aggressive
	git remote update --prune
