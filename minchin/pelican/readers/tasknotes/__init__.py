from pelican import signals

from .constants import __version__  # NOQA
from .generator import addTaskNoteArticle, pelican_finalized
from .initialize import check_settings, tasknotes_version


def register():
    """Register the plugin pieces with Pelican."""
    signals.initialized.connect(check_settings)
    signals.initialized.connect(tasknotes_version)
    signals.article_generator_pretaxonomy.connect(addTaskNoteArticle)
    signals.finalized.connect(pelican_finalized)
