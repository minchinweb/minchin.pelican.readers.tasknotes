#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from minchin.pelican.readers.commonmark.constants import COMMONMARK_DEFAULT_CONFIG
import mdit_py_plugins.anchors
import mdit_py_plugins.deflist
import minchin.md_it.fancy_tasklists

from pelican.settings import DEFAULT_CONFIG

COMMONMARK = COMMONMARK_DEFAULT_CONFIG
COMMONMARK["extensions"].extend([
    minchin.md_it.fancy_tasklists.fancy_tasklists_plugin,
    mdit_py_plugins.deflist.deflist_plugin,
    mdit_py_plugins.anchors.anchors_plugin,
])

_OUTPUT_PATH = "output"
PATH = "."  # source path
_VIRTUAL_ENVS = [
    ".venv",
    "venv",
    "__pycache__",
    ".obsidian",
    ".trash",
    "images",
    "zz_Inbox",
    "zz_test",
    "zz_test\\zz_output",
    "zz_test\\output",
    "zz_output",
    "output",
    ".zz_output",
    "zz_test\\.zz_output",
    "zz_test\\output",
    "output",

    "_templates",
]

AUTHOR = u"WM"
SITENAME = u"Jrnl Notebook"
SITEURL = "//localhost:8000"

# caching
# CACHE_CONTENT = True  # breaks on Pelican 4.7.1?
LOAD_CACHE_CONTENT = True
# LOAD_CACHE_CONTENT = False
# CHECK_MODIFIED_METHOD = "mtime"
CHECK_MODIFIED_METHOD = "md5"

TIMEZONE = "America/Edmonton"

DEFAULT_LANG = "en"
PATH_METADATA = r'(?P<category>journal|zettel|Daily)/((?P<date>\d{4}/\d{2}/\d{2}|\d{8}[0-2]\d{3}).md|.*)'
USE_FOLDER_AS_CATEGORY = False

# Feed generation is usually not desired when developing
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

STATIC_PATHS = [
    "images",
]

FAVICON = "images/favicon.ico"
FAVICON_IE = "images/favicon.ico"
SITELOGO = "images/favicon-48.png"

ELEVATOR = False

USE_PAGER = True
BOOTSTRAP_NAVBAR_INVERSE = True
DISPLAY_TAGS_INLINE = True
DISPLAY_BREADCRUMBS = True
DISPLAY_PAGES_ON_MENU = False

# A list of metadata fields containing reST/Markdown content to be parsed and translated to HTML.
FORMATTED_FIELDS = [
    "title",
    "summary",
]


PLUGINS = [
    "minchin.pelican.readers.commonmark",
    "minchin.pelican.readers.tasknotes",
    # "pelican.plugins.seafoam",
]

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
TAGS_URL = "tags/"
TAGS_SAVE_AS = "tags/index.html"
TAG_URL = "tags/{slug}/"
TAG_SAVE_AS = "tags/{slug}/index.html"
CATEGORIES_URL = "category/"
CATEGORIES_SAVE_AS = "category/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
AUTHORS_URL = None
AUTHORS_SAVE_AS = None
AUTHOR_URL = None
AUTHOR_SAVE_AS = None

ARTICLE_URL = "posts/{date:%Y}/{date:%-m}/{date:%-d}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%-m}/{date:%-d}/{slug}/index.html"
DAY_ARCHIVE_URL = "posts/{date:%Y}/{date:%-m}/{date:%-d}/"
DAY_ARCHIVE_SAVE_AS = "posts/{date:%Y}/{date:%-m}/{date:%-d}/index.html"
MONTH_ARCHIVE_URL = "posts/{date:%Y}/{date:%-m}/"
MONTH_ARCHIVE_SAVE_AS = "posts/{date:%Y}/{date:%-m}/index.html"
YEAR_ARCHIVE_URL = "posts/{date:%Y}/"
YEAR_ARCHIVE_SAVE_AS = "posts/{date:%Y}/index.html"

ARCHIVES_URL = "posts/"
ARCHIVES_SAVE_AS = "posts/index.html"

DIRECT_TEMPLATES = [
    "index",
    "categories",
    "authors",
    "archives",
    # "search",
    "tags",
    # "404",
]
PAGINATED_TEMPLATES = {
    "index": None,
    "tag": None,
    "category": None,
    "author": None,
    #"archives": None,
}
PAGINATION_PATTERNS = (
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/{number}/', '{base_name}/{number}/index.html'),
)

PAGE_PATHS = [
    "pages",
]
ARTICLE_EXCLUDES = [
    _OUTPUT_PATH,
] + PAGE_PATHS + _VIRTUAL_ENVS
PAGE_EXCLUDES = [
    _OUTPUT_PATH,
] + _VIRTUAL_ENVS

STATIC_PATHS = [
    'images',  # only default entry
]

OUTPUT_PATH = _OUTPUT_PATH

NAVBAR_ON_TOP = True
SITE_ROOT_URL = SITEURL
SEAFOAM_DEV_MODE = True  # deactivate Image Process plugin (for speed)

# import logging
# COMMONMARK_MARKDOWN_LOG_LEVEL = logging.DEBUG

TASKNOTES_FOLDER = "GTD/tasks"

# cleanup
del DEFAULT_CONFIG
del COMMONMARK_DEFAULT_CONFIG
