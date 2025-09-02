import logging

from .constants import LOG_PREFIX, __url__, __version__

logger = logging.getLogger(__name__)


def check_settings(pelican):
    """
    Insert defaults in Pelican settings, as needed.
    """
    logger.debug("%s massaging settings, setting defaults." % LOG_PREFIX)

    if "TASKNOTES_FOLDER" not in pelican.settings.keys():
        pelican.settings["TASKNOTES_FOLDER"] = "tasks"
        logger.debug(
            '%s TASKNOTES_FOLDER set to "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_FOLDER"])
        )
    else:
        logger.debug(
            '%s TASKNOTES_FOLDER previously set manually. Is "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_FOLDER"])
        )

    if "TASKNOTES_SAVE_AS" not in pelican.settings.keys():
        pelican.settings["TASKNOTES_SAVE_AS"] = pelican.settings["ARTICLE_SAVE_AS"]
        logger.debug(
            '%s TASKNOTES_SAVE_AS set to "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_SAVE_AS"])
        )
    else:
        logger.debug(
            '%s TASKNOTES_SAVE_AS previously set manually. Is "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_SAVE_AS"])
        )

    if "TASKNOTES_SLUG" not in pelican.settings.keys():
        pelican.settings["TASKNOTES_SLUG"] = "u{date:%Y%m%d%H%M}"
        logger.debug(
            '%s TASKNOTES_SLUG set to "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_SLUG"])
        )
    else:
        logger.debug(
            '%s TASKNOTES_SLUG previously set manually. Is "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_SLUG"])
        )

    if "TASKNOTES_URL" not in pelican.settings.keys():
        pelican.settings["TASKNOTES_URL"] = pelican.settings["ARTICLE_URL"]
        logger.debug(
            '%s TASKNOTES_URL set to "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_URL"])
        )
    else:
        logger.debug(
            '%s TASKNOTES_URL previously set manually. Is "%s"'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_URL"])
        )

    pelican.settings["ARTICLE_EXCLUDES"] += [
        pelican.settings["TASKNOTES_FOLDER"],
    ]
    logger.debug(
        '%s ARTICLE_EXCLUDES updated to "%s"'
        % (LOG_PREFIX, pelican.settings["ARTICLE_EXCLUDES"])
    )


def tasknotes_version(pelican):
    """
    Insert tasknotes version into Pelican context.
    """

    if "TASKNOTES_VERSION" not in pelican.settings.keys():
        pelican.settings["TASKNOTES_VERSION"] = __version__
        logger.debug(
            '%s Adding Tasknotes version "%s" to context.'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_VERSION"])
        )
    else:
        logger.debug(
            '%s TASKNOTES_VERSION already defined. Is "%s".'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_VERSION"])
        )

    if "TASKNOTES_DEV_URL" not in pelican.settings.keys():
        pelican.settings["TASKNOTES_DEV_URL"] = __url__
        logger.debug(
            '%s Adding Tasknotes Dev URL "%s" to context.'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_DEV_URL"])
        )
    else:
        logger.debug(
            '%s TASKNOTES_DEV_URL already defined. Is "%s".'
            % (LOG_PREFIX, pelican.settings["TASKNOTES_DEV_URL"])
        )
