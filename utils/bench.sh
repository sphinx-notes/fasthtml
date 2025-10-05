#!/bin/sh

# set -x
set -e

sphinx_ver=v8.2.3
sphinx_opts=-Q
mk_target=$(tail -n+25 $(git rev-parse --show-toplevel)/docs/Makefile)

pydoc_url=https://github.com/python/cpython.git
pydoc_ver=v3.13.3
pydoc_repo=cpython
pydoc_path=Doc

tmpdir=/tmp/sphinxnotes-fasthtml-bench
echo "tmpdir: $tmpdir"
if [ -z "$USE_CACHE" ]; then
    rm -rf $tmpdir || true
    mkdir -p $tmpdir || true
    cd $tmpdir
    git clone --quiet --branch $pydoc_ver --depth 1 $pydoc_url
    cd $pydoc_repo/$pydoc_path
    make venv
else
    cd $tmpdir/$pydoc_repo
    git restore .
    git clean -fd .
    cd $pydoc_path
fi

source ./venv/bin/activate

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
