#!/bin/sh

# set -x
set -e

sphinxver=v7.3.7
sphinxopts=-Q
mktarget=$(tail -n+25 $(git rev-parse --show-toplevel)/docs/Makefile)

tmpdir=$(mktemp -d)
echo "tmpdir: $tmpdir"
cd $tmpdir

python --version
python -m venv .
source ./bin/activate

pip_version() {
    python -m pip show $1 | grep Version | cut -d ' ' -f2
}

python -m pip install sphinx==$sphinxver sphinxnotes-fasthtml >/dev/null
echo "Sphinx: $(pip_version sphinx)"
echo "sphinxnotes-fasthtml: $(pip_version sphinxnotes-fasthtml)"

compare() {
    touch index.rst
    make SPHINXOPTS=$sphinxopts html
    echo ">>> Standard build"
    touch index.rst
    time make SPHINXOPTS=$sphinxopts html
    echo ">>> Fast build"
    touch index.rst
    time make SPHINXOPTS=$sphinxopts fasthtml
}

git clone --quiet --branch $sphinxver --depth 1 https://github.com/sphinx-doc/sphinx.git 2>/dev/null
cd sphinx/doc
echo "extensions.append('sphinxnotes.fasthtml')" >> conf.py
echo "$mktarget" >> Makefile
compare
cd ..

rm -rf $tmpdir
