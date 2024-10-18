"""
    sphinxnotes.fasthtml
    ~~~~~~~~~~~~~~~~~~~~

    Sphinx builder specialized for fast incremental HTML build

    :copyright: Copyright 2024 Shengyu Zhang
    :license: BSD, see LICENSE for details.

TODO:

- [ ] config-able.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util import logging
from sphinx.environment import CONFIG_CHANGED, CONFIG_EXTENSIONS_CHANGED
from sphinx.util.display import progress_message, SkipProgressMessage
from sphinx.locale import __


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
        pass  # skip gen

    @progress_message(__('writing additional pages'))
    def gen_additional_pages(self) -> None:
        raise SkipProgressMessage

    @progress_message(__('generating indices'))
    def gen_indices(self) -> None:
        """We totally skipped index generation here, but we stil need to disable
        :attr:`Builder.use_index` (see _on_builder_inited) and ``html_domain_indices``
        (see _overwrite_config), to prevent the overhead of collecting index data.
        """
        raise SkipProgressMessage

    @progress_message(__('dumping object inventory'))
    def dump_inventory(self) -> None:
        raise SkipProgressMessage

    def _overwrite_config(self) -> None:
        """
        Overwrite sphinx.config.Config to skip some operations that slow down
        the build.

        Should be called before builder.Builder.read().
        """
        self._old_config = {}

        def overwrite(name, val, optional=False, restore=True):
            if optional and not hasattr(self.config, name):
                return
            if restore:
                self._old_config[name] = getattr(self.config, name)
            setattr(self.config, name, val)

        overwrite('html_domain_indices', False, restore=False)
        # Do not build mo files.
        overwrite('gettext_auto_build', False)
        # Prevent intersphinx cache expiration.
        # See also https://github.com/sphinx-doc/sphinx/pull/12514
        overwrite('intersphinx_cache_limit', 999, optional=True)

    def _restore_config(self) -> None:
        """
        Restore sphinx.config.Config to keep sphinx.application.ENV_PICKLE_FILENAME
        unchanged.

        Must be called before pickle file is dumped to disk.
        """
        for name, val in self._old_config.items():
            setattr(self.config, name, val)
        self._old_config = {}


def _on_builder_inited(app: Sphinx):
    if not isinstance(app.builder, FastHTMLBuilder):
        return

    app.builder._overwrite_config()

    # Don't use index.
    app.builder.use_index = False
    # Disable search.
    app.builder.search = False

    # Do not update toctree.
    app.env.glob_toctrees = set()
    app.env.reread_always = set()  # marked by env.note_reread()


original_check_consistency = None
"""Original value of :meth:`BuildEnvironment.check_consistency`."""


def dummy_check_consistency() -> None:
    """Used to skip the consistency checking of Sphinx by overwriting
    :meth:`BuildEnvironment.check_consistency`.

    The function is called from :meth:`Builder.build`.
    """
    raise SkipProgressMessage


def _on_env_get_outdated(
    app: Sphinx,
    env: BuildEnvironment,
    added: set[str],
    changed: set[str],
    removed: set[str],
) -> list[str]:
    global original_check_consistency
    if not isinstance(app.builder, FastHTMLBuilder):
        # Restore check_consistency method.
        if env.check_consistency == dummy_check_consistency:
            env.check_consistency = original_check_consistency
        return []

    # Overwrite :meth:`BuildEnvironment.check_consistency` to skip consistency
    # checking.
    if env.check_consistency != dummy_check_consistency:
        original_check_consistency = env.check_consistency
        env.check_consistency = dummy_check_consistency

    # Do not trigger a full rebuild when config changed.
    if env.config_status in [CONFIG_CHANGED, CONFIG_EXTENSIONS_CHANGED]:
        # Require the env to re-calculate which docs should be rebuilt when the
        # configuration has *NOT* changed.
        added2, changed2, removed2 = env.get_outdated_files(config_changed=False)

        def clear_and_update(dst, src):
            dst.clear()
            dst.update(src)

        # sphinx.builders.Builder.read [#]_ saids "allow user intervention" when
        # emitting "env-get-outdated" signal. My understanding is that it allows
        # us to modify the docnames sets set passed in.
        #
        # .. [#]: https://github.com/sphinx-doc/sphinx/blob/v7.3.7/sphinx/builders/__init__.py#L382
        clear_and_update(added, added2)
        clear_and_update(changed, changed2)
        clear_and_update(removed, removed2)

    return []


def _on_env_updated(app: Sphinx, env: BuildEnvironment):
    if not isinstance(app.builder, FastHTMLBuilder):
        return []

    app.builder._restore_config()


def setup(app: Sphinx):
    app.connect('builder-inited', _on_builder_inited, priority=100)
    app.connect('env-get-outdated', _on_env_get_outdated)
    app.connect('env-updated', _on_env_updated)

    app.add_builder(FastHTMLBuilder)
