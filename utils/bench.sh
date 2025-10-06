#!/bin/sh

# set -x
set -e

sphinx_ver=v8.2.3
sphinx_opts=-Q
mk_target=$(tail -n+25 $(git rev-parse --show-toplevel)/docs/Makefile)

doc_url=https://github.com/sphinx-doc/sphinx.git
doc_ver=v8.2.3
doc_repo=sphinx
doc_path=doc

tmpdir=/tmp/sphinxnotes-fasthtml-bench
echo "tmpdir: $tmpdir"
if [ -z "$USE_CACHE" ]; then
    rm -rf $tmpdir || true
    mkdir -p $tmpdir || true
    cd $tmpdir
    git clone --quiet --branch $doc_ver --depth 1 $doc_url
    cd $doc_repo/$doc_path
else
    cd $tmpdir/$doc_repo
    git restore .
    git clean -fd .
    cd $doc_path
fi

python --version
python -m pip install sphinx==$sphinx_ver sphinxnotes-fasthtml >/dev/null
pip_version() {
    python -m pip show $1 | grep Version | cut -d ' ' -f2
}
echo "Sphinx: $(pip_version sphinx)"
echo "sphinxnotes-fasthtml: $(pip_version sphinxnotes-fasthtml)"

compare() {
    touch index.rst
    make SPHINXOPTS=$sphinx_opts html
    echo ">>> Standard build"
    touch index.rst
    time make SPHINXOPTS=$sphinx_opts html
    echo ">>> Fast build"
    touch index.rst
    time make SPHINXOPTS=$sphinx_opts fasthtml
}

echo "extensions.append('sphinxnotes.fasthtml')" >> conf.py
echo "$mk_target" >> Makefile
compare
cd ..

# rm -rf $tmpdir
