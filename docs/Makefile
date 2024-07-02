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

.PHONY: help Makefile default

# Catch-all target: route all unknown targets to Sphinx builder.
# $(O) is meant as a shortcut for $(SPHINXOPTS).
#
# NOTE: We want the html builder and fasthtml builder share same outdir.
#
# 	1. Don't use the make mode (-M) because it forces $(BUILDDIR)/$(BUILDERNAME)
# 		as outdir
# 	2. The $(if ...) expr returns "html" as outdir for when fasthtml builder is
# 		specified, otherwise return the original builder name
%: Makefile
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)/$(if $@=fasthtml,html,$@)" $(SPHINXOPTS) $(O) 
