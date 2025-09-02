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
_todotxt_lines = []


def addTaskNoteArticles(articleGenerator: ArticlesGenerator) -> None:
    global _tasknote_count
    global _todotxt_lines

    settings = articleGenerator.settings

    # Author, category, and tags are objects, not strings, so they need to
    # be handled using myBaseReader's process_metadata() function.
    # myBaseReader = BaseReader(settings)
    myMarkdownReader = MarkdownReader(settings)
    myBaseReader = myMarkdownReader

    file_extensions = [
        # "txt",
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

        if new_article_metadata["status"].lower() in ["in-progress", "in progress"]:
            todo_title += "[/]"
        elif new_article_metadata["status"].lower() in ["cancelled", ]:
            todo_title += "[-]"
            todotxt_line += "-"
        elif new_article_metadata["status"].lower() in ["done", ]:
            todo_title += "[x]"
            todotxt_line += "x"
        else:
            todo_title += "[ ]"

        if new_article_metadata["priority"]:
            todotxt_line += " (" + new_article_metadata["priority"].upper()[:1] + ")"

        if new_article_metadata["completed"] and new_article_metadata["date"]:
            todotxt_line += " " + new_article_metadata["completed"].format("YYYY-MM-DD")

        if new_article_metadata["date"]:
            todotxt_line += " " + new_article_metadata["date"].format("YYYY-MM-DD")

        todo_title += " " + new_article_metadata["title"]
        todotxt_line += " " + new_article_metadata["title"]

        todo_title += " ".join(["#"+x for x in new_article_metadata["tags"]])
        todotxt_line += " ".join(["+"+x for x in new_article_metadata["tags"]])

        todotxt_line += " ".join(["@"+x for x in new_article_metadata["contexts"]])

        if new_article_metadata["priority"].lower() in ["a"]:
            todo_title += " 🔺"
        elif new_article_metadata["priority"].lower() in ["b", "high"]:
            todo_title += " ⏫"
        elif new_article_metadata["priority"].lower() in ["c", "d", "n"]:
            todo_title += " 🔼"
        elif new_article_metadata["priority"].lower() in ["low", "v", "w"]:
            todo_title += " 🔽"
        elif new_article_metadata["priority"].lower() in ["z", "someday"]:
            todo_title += " ⏬️"

        if new_article_metadata["recurrance"]:
            todo_title += " 🔁" + new_article_metadata["recurrance"]
            todotxt_line += " rrule:" + new_article_metadata["recurrance"]

        if new_article_metadata["date"]:
            todo_title += " ➕" + new_article_metadata["date"].format("YYYY-MM-DD")
        
        if new_article_metadata["threshold"]:
            todo_title += " 🛫" + new_article_metadata["threshold"].format("YYYY-MM-DD")
            todotxt_line += " t:" + new_article_metadata["threshold"].format("YYYY-MM-DD")

        if new_article_metadata["scheduled"]:
            todo_title += " ⏳" + new_article_metadata["scheduled"].format("YYYY-MM-DD")

        if new_article_metadata["due"]:
            todo_title += " 📅" + new_article_metadata["due"].format("YYYY-MM-DD")
            todotxt_line += " due:" + new_article_metadata["due"].format("YYYY-MM-DD")

        if new_article_metadata["cancelled"]:
            todo_title += " ❌" + new_article_metadata["cancelled"].format("YYYY-MM-DD")

        if new_article_metadata["completed"]:
            todo_title += " ✅" + new_article_metadata["completed"].format("YYYY-MM-DD")

        if new_article_metadata["task_id"]:
            todo_title += " 🆔" + new_article_metadata["task_id"]
            todotxt_line += " id:" + new_article_metadata["task_id"]

        if new_article_metadata["depends_on"]:
            todo_title += " ⛔" + ",".join(new_article_metadata["depends_on"])
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
