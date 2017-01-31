# You can set these variables from the command line.
SPHINXOPTS      =
SPHINXBUILD     = sphinx-build
SPHINXAUTOBUILD = sphinx-autobuild
SOURCEDIR     	= .
BUILDDIR      	= _build

default:
	@echo make what?

deps:
	pip install -r requirements.txt

test:
	python -m unittest discover tests/
	pep8 finddup/ bin/ tests/

html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:
	@$(SPHINXAUTOBUILD) "$(SOURCEDIR)" "$(BUILDDIR)"/html $(SPHINXOPTS) -r ".git/.*" $(O)
