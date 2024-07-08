#!/bin/sh

# set -x
set -e

sphinxver=v7.3.7
mktarget=$(tail -n+25 $(git rev-parse --show-toplevel)/docs/Makefile)

tmpdir=$(mktemp -d)
echo $tmpdir
cd $tmpdir

python --version
python -m venv .
source ./bin/activate

python -m pip install sphinx==$sphinxver sphinxnotes-fasthtml >/dev/null
pip show sphinx sphinxnotes-fasthtml

compare() {
    echo "" >> index.rst
    make SPHINXOPTS=-Q html
    echo ">>> Standard build"
    echo "Another line" >> index.rst
    time make SPHINXOPTS=-Q html
    echo ">>> Fast build"
    echo "Another line" >> index.rst
    time make SPHINXOPTS=-Q fasthtml
}

echo "=== Sphinx"
git clone --quiet --branch $sphinxver --depth 1 https://github.com/sphinx-doc/sphinx.git >/dev/null
cd sphinx/doc
echo "extensions.append('sphinxnotes.fasthtml')" >> conf.py
echo $mktarget >> Makefile
compare
cd ..

# rm -rf $tmpdir
