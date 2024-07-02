.. This file is generated from sphinx-notes/cookiecutter.
   You need to consider modifying the TEMPLATE or modifying THIS FILE.

.. include:: ../README.rst

Introduction
============

.. ADDITIONAL CONTENT START

A Sphinx builder specialized for **fast incremental HTML** build.

The builtin HTML builder (``StandaloneHTMLBuilder``) supports incremental build
too, but it have to do a lot of extra work to ensure document consistency, such
as: updating glob toctree, updating domain index, deal with config changed, and
so on. The fasthtml builder wraps the builtin one and **skips almost all
operations that slow down the build** and left only the necessary parts.

If you often need to edit and build Sphinx documents locally, and you only want
to preview the parts you modified, the fasthtml builder will be helpful to you. 

.. ADDITIONAL CONTENT END

Getting Started
===============

.. note::

   We assume you already have a Sphinx documentation,
   if not, see `Getting Started with Sphinx`_.

First, downloading extension from PyPI:

.. code-block:: console

   $ pip install sphinxnotes-fasthtml

Then, add the extension name to ``extensions`` configuration item in your conf.py_:

.. code-block:: python

   extensions = [
             # …
             'sphinxnotes.fasthtml',
             # …
             ]

.. _Getting Started with Sphinx: https://www.sphinx-doc.org/en/master/usage/quickstart.html
.. _conf.py: https://www.sphinx-doc.org/en/master/usage/configuration.html

.. ADDITIONAL CONTENT START

Then you can run the builder:

.. code-block:: console

   $ sphinx-build -b fasthtml <sourcedir> <outputdir>

For users who build document through Makefile, it is recommended to modify the
catch-all target as following:

.. literalinclude:: Makefile
   :language: make
   :lines: 20-

.. ADDITIONAL CONTENT END

Contents
========

.. toctree::
   :caption: Contents

   changelog

The Sphinx Notes Project
========================

The project is developed by `Shengyu Zhang`__,
as part of **The Sphinx Notes Project**.

.. toctree::
   :caption: The Sphinx Notes Project

   Home <https://sphinx.silverrainz.me/>
   Blog <https://silverrainz.me/blog/category/sphinx.html>
   PyPI <https://pypi.org/search/?q=sphinxnotes>

__ https://github.com/SilverRainZ
