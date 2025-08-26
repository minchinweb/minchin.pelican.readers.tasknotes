from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pelican import Pelican
    from pelican.generators import ArticlesGenerator

from jinja2.utils import url_quote

from pelican.contents import Article
from pelican.readers import MarkdownReader  # BaseReader
from pelican.utils import order_content

from .constants import DEFAULT_TASKNOTES_CATEGORY, LOG_PREFIX

# from pelican.utils import get_date, pelican_open


logger = logging.getLogger(__name__)

_tasknote_count = 0


def addTaskNoteArticle(articleGenerator: ArticlesGenerator) -> None:
    global _tasknote_count

    settings = articleGenerator.settings

    # Author, category, and tags are objects, not strings, so they need to
    # be handled using myBaseReader's process_metadata() function.
    # myBaseReader = BaseReader(settings)
    myMarkdownReader = MarkdownReader(settings)
    myBaseReader = myMarkdownReader

    file_extensions = [
        "txt",
    ] + MarkdownReader.file_extensions

    for post in articleGenerator.get_files(
        paths=settings["TASKNOTES_FOLDER"], extensions=file_extensions
    ):
        post = settings["PATH"] + os.sep + post

        content, metadata = myMarkdownReader.read(source_path=post)

        new_article_metadata = {
            "category": myBaseReader.process_metadata(
                "category",
                settings.get("TASKNOTES_CATEGORY", DEFAULT_TASKNOTES_CATEGORY),
            ),
            # "tags": myBaseReader.process_metadata("tags", "tagA, tagB"),
            "tasknote": myBaseReader.process_metadata("tasknote", True),
        }

        post_slug = settings["TASKNOTES_SLUG"].format(**metadata)
        metadata["slug"] = post_slug

        try:
            new_article_metadata["author"] = myBaseReader.process_metadata(
                "author", settings["AUTHOR"]
            )
        except KeyError:
            # if author isn't set by either the general settings or the
            # micropost metadata, we don't need to force one
            pass

        new_article_metadata["title"] = myBaseReader.process_metadata(
            "title", post_slug
        )
        new_article_metadata["date"] = metadata["date"]
        new_article_metadata["slug"] = post_slug
        new_article_metadata["save_as"] = myBaseReader.process_metadata(
            "save_as", settings["TASKNOTES_SAVE_AS"].format(**metadata)
        )
        new_article_metadata["url"] = myBaseReader.process_metadata(
            "url", settings["TASKNOTES_URL"].format(**metadata)
        )

        if "image" in metadata.keys():
            new_article_metadata["image"] = myBaseReader.process_metadata(
                "image", metadata["image"]
            )

            # add image link to end of content

            image_url = f'{settings["SITEURL"]}'
            image_url += "/" if not settings["SITEURL"].endswith("/") else ""
            image_url += url_quote(metadata["image"])  # Jinja filter "urlencode"

            image_link = f'<a href={image_url} class="microblog-post-image">{image_url}</a>'

            content = content.removesuffix("</p>") + " " + image_link + "</p>"

        if "tags" in metadata.keys():
            # new_article_metadata["tags"] = myBaseReader.process_metadata("tags", metadata["tags"])
            new_article_metadata["tags"] = metadata["tags"]

            if settings.get("MICROBLOG_APPEND_HASHTAGS", True):
                # metadata["tags"] is already a list of `pelican.urlwrappers.Tag`
                for tag in metadata["tags"]:
                    tag_url = settings["SITEURL"] + "/" + tag.url
                    tag_link = f'<a href="{tag_url}" class="microblog-post-tag">#{tag.name}</a>'

                    content = content.removesuffix("</p>") + " " + tag_link + "</p>"


        # NOTE:
        # new_article_metadata is set by pelicanconf.py
        # metadata is set from the tasknote and is given higher precedence below.
        new_article_metadata.update(metadata)

        new_article = Article(
            content,
            new_article_metadata,
        )

        articleGenerator.articles.insert(0, new_article)
        _tasknote_count += 1

    # apply sorting
    logger.debug(f'{LOG_PREFIX} sorting order: "{settings.get("ARTICLE_ORDER_BY", "reversed-date")}"')
    articleGenerator.articles = order_content(
        articleGenerator.articles, settings.get("ARTICLE_ORDER_BY", "reversed-date")
    )


def pelican_finalized(pelican: Pelican) -> None:
    global _tasknote_count
    print(
        "%s Processed %s tasknote%s."
        % (LOG_PREFIX, _tasknote_count, "s" if _tasknote_count != 1 else ""),
    )
