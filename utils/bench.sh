#!/bin/sh

# set -x
set -e

tmpdir=$(mktemp -d)
echo $tmpdir
cd $tmpdir

python --version
python -m venv .
source ./bin/activate

python -m pip install sphinx==v7.3.7 sphinxnotes-fasthtml >/dev/null
pip show sphinx sphinxnotes-fasthtml

compare() {
    echo "" >> index.rst
    make SPHINXOPTS=-Q html
    echo ">>> Fast build"
    echo "Another line" >> index.rst
    time make SPHINXOPTS=-Q fast
    echo ">>> Standard build"
    echo "Another line" >> index.rst
    time make SPHINXOPTS=-Q html
}

echo "=== Sphinx"
git clone --quiet --branch v7.3.7 --depth 1 https://github.com/sphinx-doc/sphinx.git >/dev/null
cd sphinx/doc
echo "extensions.append('sphinxnotes.fasthtml')" >> conf.py
cat <<'EOF' >> Makefile
fast: Makefile
	@$(SPHINXBUILD) -b fasthtml "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
EOF
compare
cd ..

# rm -rf $tmpdir
