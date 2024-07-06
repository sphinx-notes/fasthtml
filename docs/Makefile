# This file is generated from sphinx-notes/cookiecutter.
# You need to consider modifying the TEMPLATE or modifying THIS FILE.

# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python3 -msphinx
SOURCEDIR     = .
BUILDDIR      = _build

default: fast

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile default fast

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

fast: Makefile
	@$(SPHINXBUILD) -b fasthtml "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
