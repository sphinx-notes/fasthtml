"""
    sphinxnotes.fasthtml
    ~~~~~~~~~~~~~~~~~~~~

    Sphinx builder specialized for fast incremental HTML build 

    :copyright: Copyright 2024 Shengyu Zhang
    :license: BSD, see LICENSE for details.

TODO:

- [ ] skip 'checking consistency'
- [ ] why always [config changed ('gettext_auto_build')]?
- [ ] config-able.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging
from sphinx.environment import CONFIG_OK

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment

logger = logging.getLogger(__name__)

class FastHTMLBuilder(StandaloneHTMLBuilder):
    name = 'fasthtml'

    def __init__(self, app: Sphinx, env: BuildEnvironment) -> None:
        # We only use the 'fasthtml' for registering builder,
        # then continue to use the same name as StandaloneHTMLBuilder,
        # to ensure that the behavior with StandaloneHTMLBuilderi as same
        # as possible.
        #
        # Otherwise, different builde name causes troubles: 
        #
        # - Builder.tags will be different (see Builder.init()), which leads
        #   to BuildInfo changes, finally leads Builder.get_outdated_docs()
        #   returns all docs and do a full rebuild.
        # - sphinxnotes-any (another project of mine) creates a directory for
        #   storing intermediate files according to builder name (.any_xxx/),
        #   if builder names are different, intermediate files can't be shared
        #   between {Fast,Standalone}HTMLBuilder, which leas to unnecessary
        #   rebuild.
        self.name = StandaloneHTMLBuilder.name
        super().__init__(app, env)


    def gen_pages_from_extensions(self) -> None:
        pass # skip gen


def _on_builder_inited(app: Sphinx):
    if not isinstance(app.builder, FastHTMLBuilder):
        return

    # Disable general index.
    app.config.html_use_index = False # type: ignore
    app.builder.use_index = False
    # Disable domain-specific indices.
    app.config.html_domain_indices = False # type: ignore

    # Disable search.
    app.builder.search = False

    # Do not update toctree.
    app.env.glob_toctrees = set()
    app.env.reread_always = set() # marked by env.note_reread()

    # Do not build mo files.
    app.config.gettext_auto_build = False # type: ignore


def _on_env_get_outdated(app: Sphinx, env: BuildEnvironment, added: set[str],
                         changed: set[str], removed: set[str]) -> list[str]:
    if not isinstance(app.builder, FastHTMLBuilder):
        return []

    # Config changes causes a fully rebuild, I don't want this.
    if env.config_status != CONFIG_OK:
        # Require the env to recalculate which docs should be rebuilt when the
        # configuration has *NOT* changed.
        added2, changed2, removed2 = env.get_outdated_files(config_changed=False)

        def clear_and_update(dst, src):
            dst.clear(); dst.update(src)
        # sphinx.builders.Builder.read [#]_ saids "allow user intervention" when
        # emitting "env-get-outdated" signal. My understanding is that it allows
        # us to modify the docnames sets set passed in.
        #
        # .. [#]: https://github.com/sphinx-doc/sphinx/blob/v7.3.7/sphinx/builders/__init__.py#L382
        clear_and_update(added, added2)
        clear_and_update(changed, changed2)
        clear_and_update(removed, removed2)

    return []

def setup(app: Sphinx):
    app.connect('builder-inited', _on_builder_inited, priority=100)
    app.connect('env-get-outdated', _on_env_get_outdated)

    app.add_builder(FastHTMLBuilder)
