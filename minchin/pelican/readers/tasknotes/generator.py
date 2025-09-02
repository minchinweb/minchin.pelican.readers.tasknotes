from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pelican import Pelican
    from pelican.generators import ArticlesGenerator

from pelican.contents import Article
# from pelican.readers import MarkdownReader  # BaseReader
from pelican.utils import order_content

from minchin.pelican.readers.commonmark.reader import MDITReader

from .constants import DEFAULT_TASKNOTES_CATEGORY, LOG_PREFIX

# from pelican.utils import get_date, pelican_open


logger = logging.getLogger(__name__)

_tasknote_count = 0
_todotxt_lines = []


def addTaskNoteArticles(articleGenerator: ArticlesGenerator) -> None:
    global _tasknote_count
    global _todotxt_lines

    settings = articleGenerator.settings

    # Author, category, and tags are objects, not strings, so they need to
    # be handled using myBaseReader's process_metadata() function.
    # myBaseReader = BaseReader(settings)
    # myMarkdownReader = MarkdownReader(settings)
    myMarkdownReader = MDITReader(settings)
    myBaseReader = myMarkdownReader

    file_extensions = [
        # "txt",
    ] + myMarkdownReader.file_extensions

    for post in articleGenerator.get_files(
        paths=settings["TASKNOTES_FOLDER"], extensions=file_extensions
    ):
        post = settings["PATH"] + os.sep + post

        # content, metadata = myMarkdownReader.read(source_path=post)
        content, metadata = myMarkdownReader.read(filename=post)

        logger.debug(f"{LOG_PREFIX} {metadata}")

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

        if "tags" in metadata.keys():
            # new_article_metadata["tags"] = myBaseReader.process_metadata("tags", metadata["tags"])
            new_article_metadata["tags"] = metadata["tags"]

            if settings.get("TASKNOTES_APPEND_HASHTAGS", True):
                # metadata["tags"] is already a list of `pelican.urlwrappers.Tag`
                for tag in metadata["tags"]:
                    tag_url = settings["SITEURL"] + "/" + tag.url
                    tag_link = f'<a href="{tag_url}" class="tasknotes-post-tag">#{tag.name}</a>'

                    content = content.removesuffix("</p>") + " " + tag_link + "</p>"


        # Assemble Tasks-style line
        # this is the presented as the "title" of the todo item, with various
        # metadata directly embedded. Example:
        # - [x] take out the trash #tags 🆔 abcdef ⛔ ghijkl 🔺/⏫/🔼/ /🔽/⏬️
        #   🔁 every Sunday ➕ 2021-04-09 🛫 2021-04-09 ⏳ 2021-04-09
        #   📅 2021-04-09 ❌ 2021-04-09 ✅ 2021-04-09 ⏰ YYYY-MM-DD HH:mm
        todo_title = ""

        # this is the todo item, as would be read in the todo.txt format
        todotxt_line = ""

        if "status" not in new_article_metadata:
            pass
        elif new_article_metadata["status"].lower() in ["in-progress", "in progress"]:
            todo_title += '<span title="In Progress">[/]</span>'
        elif new_article_metadata["status"].lower() in ["cancelled", ]:
            todo_title += '<span title="Cancelled">[-]</span>'
            todotxt_line += "-"
        elif new_article_metadata["status"].lower() in ["done", ]:
            todo_title += '<span title="Done!">[x]</span>'
            todotxt_line += "x"
        else:
            todo_title += '<span title="Open">[ ]</span>'


        if "priority" in new_article_metadata:
            todotxt_line += " (" + new_article_metadata["priority"].upper()[:1] + ")"

        if "completed" in new_article_metadata and new_article_metadata["completed"] and new_article_metadata["date"]:
            todotxt_line += " " + new_article_metadata["completed"].strftime("%Y-%m-%d")

        if new_article_metadata["date"]:
            todotxt_line += " " + new_article_metadata["date"].strftime("%Y-%m-%d")

        todo_title += " " + new_article_metadata["title"]
        todotxt_line += " " + new_article_metadata["title"]

        todo_title += " ".join(["#"+tag.name for tag in new_article_metadata["tags"]])
        todotxt_line += " ".join(["+"+tag.name for tag in new_article_metadata["tags"]])

        if "contexts" in new_article_metadata:
            if isinstance(new_article_metadata["contexts"], list):
                todotxt_line += " ".join(["@"+x for x in new_article_metadata["contexts"]])
            elif isinstance(new_article_metadata["contexts"], str):
                todotxt_line += " @" + new_article_metadata["contexts"]

        if "priority" not in new_article_metadata:
            pass
        elif new_article_metadata["priority"].lower() in ["a"]:
            todo_title += ' <span title="Highest Priority">🔺</span>'
        elif new_article_metadata["priority"].lower() in ["b", "high"]:
            todo_title += ' <span title="High Priority">⏫</span>'
        elif new_article_metadata["priority"].lower() in ["c", "d", "n"]:
            todo_title += ' <span title="Medium Priority">🔼</span>'
        elif new_article_metadata["priority"].lower() in ["low", "v", "w"]:
            todo_title += ' <span title="Low Priority">🔽</span>'
        elif new_article_metadata["priority"].lower() in ["z", "someday"]:
            todo_title += ' <span title="Lowest Priority">⏬️</span>'

        if "recurrance" in new_article_metadata:
            todo_title += '<span title="Recurrance">🔁</span>' + new_article_metadata["recurrance"]
            todotxt_line += " rrule:" + new_article_metadata["recurrance"]

        if new_article_metadata["date"]:
            todo_title += '<span title="Created Date">➕</span>' + new_article_metadata["date"].strftime("%Y-%m-%d")
        
        if "threshold" in new_article_metadata:
            todo_title += '<span title="Threshold (Start) Date">🛫</span>' + new_article_metadata["threshold"].strftime("%Y-%m-%d")
            todotxt_line += " t:" + new_article_metadata["threshold"].strftime("%Y-%m-%d")

        if "scheduled" in new_article_metadata:
            todo_title += '<span title="Scheduled Date">⏳</span>' + new_article_metadata["scheduled"].strftime("%Y-%m-%d")

        if "due" in new_article_metadata:
            todo_title += '<span title="Due Date">📅</span>' + new_article_metadata["due"].strftime("%Y-%m-%d")
            todotxt_line += " due:" + new_article_metadata["due"].strftime("%Y-%m-%d")

        if "cancelled" in new_article_metadata:
            todo_title += '<span title="Date Cancelled">❌</span>' + new_article_metadata["cancelled"].strftime("%Y-%m-%d")

        if "completed" in new_article_metadata:
            todo_title += '<span title="Date Completed">✅</span>' + new_article_metadata["completed"].strftime("%Y-%m-%d")

        if "task_id" in new_article_metadata:
            todo_title += '<span title="Task ID">🆔</span>' + new_article_metadata["task_id"]
            todotxt_line += " id:" + new_article_metadata["task_id"]

        if "depends_on" in new_article_metadata:
            todo_title += '<span title="Depends On">⛔</span>' + ",".join(new_article_metadata["depends_on"])
            todotxt_line += " depends_on:" + ",".join(new_article_metadata["depends_on"])

        new_article_metadata["summary"] = todo_title


        # NOTE:
        # new_article_metadata is set by pelicanconf.py
        # metadata is set from the tasknote and is given higher precedence below.
        new_article_metadata.update(metadata)

        new_article = Article(
            content,
            new_article_metadata,
        )

        articleGenerator.articles.insert(0, new_article)
        logger.debug(f"{LOG_PREFIX} {todotxt_line}")
        _todotxt_lines.append(todotxt_line)
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
