from pelican import signals

from .constants import __version__  # NOQA
from .generator import addTaskNoteArticles, pelican_finalized
from .initialize import check_settings, tasknotes_version


def register():
    """Register the plugin pieces with Pelican."""
    signals.initialized.connect(check_settings)
    signals.initialized.connect(tasknotes_version)
    signals.article_generator_pretaxonomy.connect(addTaskNoteArticles)
    signals.finalized.connect(pelican_finalized)


# TODO: write todo.txt file; may need to extend "Everything" Writer
