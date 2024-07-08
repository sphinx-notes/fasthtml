# This file is generated from sphinx-notes/cookiecutter.
# You need to consider modifying the TEMPLATE or modifying THIS FILE.

# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python3 -msphinx
SOURCEDIR     = .
BUILDDIR      = _build

default: fasthtml

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile default fast

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Without "make mode" we can specify OUTPUTDIR and DOCTREEDIR precisely
# so that we can make sure to share all output with the HTML builder.
fasthtml: Makefile
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O) -d "$(BUILDDIR)/doctrees"
