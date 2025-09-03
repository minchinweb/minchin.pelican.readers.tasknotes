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

        new_article_metadata["title"] = metadata["title"]
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

        if "task_status" in metadata.keys():
            new_article_metadata["status"] = metadata["task_status"]
        elif "status" in metadata.keys():
            new_article_metadata["status"] = metadata["status"]

        if "priority" in metadata.keys():
            new_article_metadata["priority"] = metadata["priority"]
        if "completed" in metadata.keys():
            new_article_metadata["completed"] = metadata["completed"]
        # TODO: This should be a list
        if "contexts" in metadata.keys():
            new_article_metadata["contexts"] = metadata["contexts"]
        # TODO: This should be a list
        if "projects" in metadata.keys():
            new_article_metadata["projects"] = metadata["projects"]
        if "recurrance" in metadata.keys():
            new_article_metadata["recurrance"] = metadata["recurrance"]

        if "threshold_date" in metadata.keys():
            new_article_metadata["threshold"] = metadata["threshold_date"]
        elif "threshold" in metadata.keys():
            new_article_metadata["threshold"] = metadata["threshold"]
            
        if "scheduled" in metadata.keys():
            new_article_metadata["scheduled"] = metadata["scheduled"]
        if "due" in metadata.keys():
            new_article_metadata["due"] = metadata["due"]
        if "cancelled" in metadata.keys():
            new_article_metadata["cancelled"] = metadata["cancelled"]
        if "completed" in metadata.keys():
            new_article_metadata["completed"] = metadata["completed"]
        # TODO: derive this from the timename??
        if "task_id" in metadata.keys():
            new_article_metadata["task_id"] = metadata["task_id"]
        # TODO: this should be a list
        if "depends_on" in metadata.keys():
            new_article_metadata["depends_on"] = metadata["depends_on"]


        # Assemble Tasks-style line
        # this is the presented as the "title" of the todo item, with various
        # metadata directly embedded. Example:
        # - [x] take out the trash #tags 🆔 abcdef ⛔ ghijkl 🔺/⏫/🔼/ /🔽/⏬️
        #   🔁 every Sunday ➕ 2021-04-09 🛫 2021-04-09 ⏳ 2021-04-09
        #   📅 2021-04-09 ❌ 2021-04-09 ✅ 2021-04-09 ⏰ YYYY-MM-DD HH:mm
        todo_title = ""

        # this is the todo item, as would be read in the todo.txt format
        todotxt_line = ""

        _data_task = " "
        # These checkboxes match the formatting from my Fancy-Checkboxes plugin
        # for Markdown-IT. They will need to be styled by the theme in use.
        if "status" not in new_article_metadata:
            pass
        elif new_article_metadata["status"].lower() in ["in-progress", "in progress"]:
            _data_task = "/"
        elif new_article_metadata["status"].lower() in ["cancelled", ]:
            _data_task = "-"
            todotxt_line += "-"  # TODO: is this the right way to show this??
        elif new_article_metadata["status"].lower() in ["done", ]:
            _data_task = "x"
            todotxt_line += "x "
        else:
            # _data_task = " "
            pass

        _todo_checkbox = ""
        _todo_checkbox += '<input class="task-list-item-checkbox" '
        _todo_checkbox += 'disabled="disabled" type="checkbox" data-task="'
        _todo_checkbox += _data_task
        _todo_checkbox += '" /><span data-task="'
        _todo_checkbox += _data_task
        _todo_checkbox += '"></span>'

        new_article_metadata["tasknote_checkbox"] = _todo_checkbox
        todo_title += _todo_checkbox

        # priorities are removed from completed items, so they sort to the bottom
        if "priority" in new_article_metadata and "completed" not in new_article_metadata:
            todotxt_line += "(" + new_article_metadata["priority"].upper()[:1] + ") "

        if "completed" in new_article_metadata and new_article_metadata["completed"] and new_article_metadata["date"]:
            todotxt_line += new_article_metadata["completed"].strftime("%Y-%m-%d") + " "

        if new_article_metadata["date"]:
            todotxt_line += new_article_metadata["date"].strftime("%Y-%m-%d") + " "

        todo_title += " " + new_article_metadata["title"]
        todotxt_line += new_article_metadata["title"] + " "

        # TODO: Render as a link (a project should have a rendered page (or
        # post))
        # TODO: Process Wikilinks here
        if "projects" in new_article_metadata:
            if isinstance(new_article_metadata["projects"], list):
                todo_title += " " + " ".join(["+"+x for x in new_article_metadata["projects"]])
                todotxt_line += " ".join(["+"+x for x in new_article_metadata["projects"]]) + " "
            elif isinstance(new_article_metadata["projects"], str):
                todo_title += " +" + new_article_metadata["projects"]
                todotxt_line += new_article_metadata["projects"] + " "

        if "tags" in metadata.keys():
            # metadata["tags"] is already a list of `pelican.urlwrappers.Tag`
            for tag in metadata["tags"]:
                tag_url = settings["SITEURL"] + "/" + tag.url
                tag_link = f'<a href="{tag_url}" class="tasknotes-tag">#{tag.name}</a>'
                todo_title += " " + tag_link
        todotxt_line += " ".join(["#"+tag.name for tag in new_article_metadata["tags"]]) + " "

        if "contexts" in new_article_metadata:
            if isinstance(new_article_metadata["contexts"], list):
                todo_title += " " + " ".join(["@"+x for x in new_article_metadata["contexts"]])
                todotxt_line += " ".join(["@"+x for x in new_article_metadata["contexts"]]) + " "
            elif isinstance(new_article_metadata["contexts"], str):
                todo_title += " " + " @" + new_article_metadata["contexts"]
                todotxt_line += " @" + new_article_metadata["contexts"] + " "

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
            todo_title += ' <span title="Recurrance">🔁</span>' + new_article_metadata["recurrance"]
            todotxt_line += "rrule:" + new_article_metadata["recurrance"] + " "

        if new_article_metadata["date"]:
            todo_title += ' <span title="Created Date">➕</span><time datetime="' + new_article_metadata["date"].isoformat() + '">' + new_article_metadata["date"].strftime("%Y-%m-%d") + '</time>'
        
        if "threshold" in new_article_metadata:
            todo_title += ' <span title="Threshold (Start) Date">🛫</span><time datetime="' + new_article_metadata["threshold"].isoformat() + '">' + new_article_metadata["threshold"].strftime("%Y-%m-%d") + '</time>'
            todotxt_line += "t:" + new_article_metadata["threshold"].strftime("%Y-%m-%d") + " "

        if "scheduled" in new_article_metadata:
            todo_title += ' <span title="Scheduled Date">⏳</span><time datetime="' + new_article_metadata["scheduled"].isoformat() + '">' + new_article_metadata["scheduled"].strftime("%Y-%m-%d") + '</time>'

        if "due" in new_article_metadata:
            todo_title += ' <span title="Due Date">📅</span><time datetime="' + new_article_metadata["due"].isoformat() + '">' + new_article_metadata["due"].strftime("%Y-%m-%d") + '</time>'
            todotxt_line += "due:" + new_article_metadata["due"].strftime("%Y-%m-%d") + " "

        # Cancelled tasks don't have a "cancelled date", but are given a
        # `(task_)status` of "`cancelled` and marked `completed` on the date
        # they are cancelled.
        if "status" in new_article_metadata and new_article_metadata["status"].lower() == "cancelled" and "completed" in new_article_metadata:
            todo_title += ' <span title="Date Cancelled">❌</span><time datetime="' + new_article_metadata["completed"].isoformat() + '">' + new_article_metadata["completed"].strftime("%Y-%m-%d") + '</time>'
        # Tasks are assumed to be be both "Completed" (successfully) and
        # "Cancelled"
        elif "completed" in new_article_metadata:
            todo_title += ' <span title="Date Completed">✅</span><time datetime="' + new_article_metadata["completed"].isoformat() + '">' + new_article_metadata["completed"].strftime("%Y-%m-%d") + '</time>'

        if "task_id" in new_article_metadata:
            todo_title += ' <span title="Task ID">🆔</span>' + new_article_metadata["task_id"]
            todotxt_line += "id:" + new_article_metadata["task_id"] + " "

        # TODO: render these as links to the other todo items
        if "depends_on" in new_article_metadata:
            todo_title += ' <span title="Depends On">⛔</span>' + ",".join(new_article_metadata["depends_on"])
            # 'p:' for "parent"
            todotxt_line += "p:" + ",".join(new_article_metadata["depends_on"]) + " "

        # move trailing space, if any
        todotxt_line = todotxt_line.rstrip()

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
