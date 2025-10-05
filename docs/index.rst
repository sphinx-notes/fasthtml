.. This file is generated from sphinx-notes/cookiecutter.
   You need to consider modifying the TEMPLATE or modifying THIS FILE.

====================
sphinxnotes-fasthtml
====================

.. |docs| image:: https://img.shields.io/github/deployments/sphinx-notes/fasthtml/github-pages?label=docs
   :target: https://sphinx.silverrainz.me/fasthtml
   :alt: Documentation Status
.. |license| image:: https://img.shields.io/github/license/sphinx-notes/fasthtml
   :target: https://github.com/sphinx-notes/fasthtml/blob/master/LICENSE
   :alt: Open Source License
.. |pypi| image:: https://img.shields.io/pypi/v/sphinxnotes-fasthtml.svg
   :target: https://pypi.python.org/pypi/sphinxnotes-fasthtml
   :alt: PyPI Package
.. |download| image:: https://img.shields.io/pypi/dm/sphinxnotes-fasthtml
   :target: https://pypi.python.org/pypi/sphinxnotes-fasthtml
   :alt: PyPI Package Downloads
.. |github| image:: https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white/
   :target: https://github.com/sphinx-notes/fasthtml
   :alt: GitHub Repository

|docs| |license| |pypi| |download| |github|

Introduction
============

.. INTRODUCTION START

A Sphinx builder specialized for **fast incremental HTML** build.

Sphinx's HTML builder does a lot of works to ensure document consistency
(such as updating glob toctree, updating index, etc.) The fasthtml builder
**skips almost all operations that slow down the build** and left only the
necessary parts.

If you only want the document you modified to be updated, without paying
attention to the consistency of other places, the fasthtml builder will be
helpful to you.

.. note::

   This extension relies on the internal implementation of HTML builder
   (:py:class:`~sphinx.builders.html.StandaloneHTMLBuilder`), it may not be
   compatible with older or future Sphinx versions.

   So **DO NOT report to Sphinx first if you suffered crash**, please report to
   here :issue:`new` instead.

.. INTRODUCTION END

Getting Started
===============

.. note::

   We assume you already have a Sphinx documentation,
   if not, see `Getting Started with Sphinx`_.


First, downloading extension from PyPI:

.. code-block:: console

   $ pip install sphinxnotes-fasthtml


Then, add the extension name to ``extensions`` configuration item in your
:parsed_literal:`conf.py_`:

.. code-block:: python

   extensions = [
             # …
             'sphinxnotes.fasthtml',
             # …
             ]

.. _Getting Started with Sphinx: https://www.sphinx-doc.org/en/master/usage/quickstart.html
.. _conf.py: https://www.sphinx-doc.org/en/master/usage/configuration.html

.. ADDITIONAL CONTENT START

Then you can run the ``fasthtml`` builder:

.. code-block:: console

   $ sphinx-build -b fasthtml <sourcedir> <outputdir>

For Makefile users, it is recommended to add the following lines to your
Makefile, to share ``outputdir`` betweens the ``fasthtml`` builder and the
builtin ``html`` builder:

.. literalinclude:: Makefile
   :language: make
   :lines: 25-

Then use ``make fasthtml`` to run the fast HTML build.

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
