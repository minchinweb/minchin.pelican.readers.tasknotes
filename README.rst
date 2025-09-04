========================
Pelican Tasknotes Reader
========================

*A Pelican plugin providing "task notes" capabilities.*

.. image:: https://img.shields.io/pypi/v/minchin.pelican.readers.tasknotes.svg?style=flat
   :target: https://pypi.python.org/pypi/minchin.pelican.readers.tasknotes/
   :alt: PyPI version number

.. image:: https://img.shields.io/badge/-Changelog-success
   :target: https://github.com/MinchinWeb/minchin.pelican.readers.tasknotes/blob/master/CHANGELOG.rst
   :alt: Changelog

.. image:: https://img.shields.io/pypi/pyversions/minchin.pelican.readers.tasknotes?style=flat
   :target: https://pypi.python.org/pypi/minchin.pelican.readers.tasknotes/
   :alt: Supported Python version

.. image:: https://img.shields.io/pypi/l/minchin.pelican.readers.tasknotes.svg?style=flat&color=green
   :target: https://github.com/MinchinWeb/minchin.pelican.readers.tasknotes/blob/master/LICENSE.txt
   :alt: License

.. image:: https://img.shields.io/pypi/dm/minchin.pelican.readers.tasknotes.svg?style=flat
   :target: https://pypi.python.org/pypi/minchin.pelican.readers.tasknotes/
   :alt: Download Count

Quickstart
----------

1. Install the plugin via pip: ``pip install minchin.pelican.readers.tasknotes``
2. Generally, the plugin should be loaded and configured automatically without
   further effort on your part.
3. Create a ``tasks`` folder in your content folder (to hold your tasknotes!).
4. Create a new "post" in your ``tasks`` folder. This file will mostly be
   metadata, but the ``title`` and ``date`` are the only mandatory fields (and,
   depending on how you're configured Pelican, you might be able to read the
   ``date`` from the filesystem, making it not needed either!) You can also
   provide a text body, which will be read as Markdown (so plain text
   effectively works too)!
5. Regenerate your Pelican site!

Sample (Tasknote) "Post" File
-----------------------------

.. code-block:: md

   <!-- ./content/micro/202307091701.md -->

   date: 2023-07-09 17:01

   I'm microblogging with Pelican!
   https://blog.minchin.ca/label/microblogging-pelican

Or a post with an image:

.. code-block:: md

   <!-- ./content/micro/202307112138.md -->

   date: 2023-07-11 21:38
   image: images/birger-strahl-olI66vtMgNo-unsplash.jpg

   Microblog posts can have "feature" images too! (URL of photo should
   automatically be added.)

The image path is relative to your ``content`` folder. A URL of the photo is
added to the end of the post as well.

Or with tags (or hashtags):

.. code-block:: md

   <!-- ./content/micro/202307131456.md -->

   date: 2023-07-13 14:56
   tags: Python, Pelican, Microblogging

   I'm now Microblogging with Pelican!


This will add links at the end of your post to the tags to the tag page for
your (Pelican) site.

For now, it does not pull tags out of the body of your post.

Background Notes
----------------

This format is based on the format used by the Obsidian `TaskNotes
<https://callumalpass.github.io/tasknotes/>_` plugin. The basic idea is that
each task (or "todo item") is its own file. On one hand, this leads to a ton of
small files, but it does make it easy to filter and search based on file
properties. One additional advantage over relying on inline todos (in other
notes), is that note about the todo item can be stored in the tasknote itself.

Nothing in this reader relies on Obsidian or the TaskNotes (Obsidian) plugin,
nor does this reader implement any of the specialized views of the TaskNote
plugin.

Installation
------------

The easiest way to installed *TaskNotes* is through ``pip``:

.. code-block:: sh

   pip install minchin.pelican.reader.tasknotes

Requirements
------------

*Tasknotes* relies on Pelican, and the ``autoloader`` plugin (for autoloading).
If this plugin is installed from PyPI, these should automatically be installed.

If you need to insrall them manually:

.. code-block:: sh

   pip install pelican
   pip install minchin.pelican.plugins.autoloader

..
    Additional Images
    -----------------

    Tasknotes "post", using the Seafoam theme:

    (Placeholder image for the moment...)

    .. image:: https://github.com/MinchinWeb/seafoam/raw/master/docs/screenshots/2.6.0/article_with_header.png
    :align: center
    :alt: Replace Image...


Pelican Settings
----------------

These settings can be set in your ``pelicanconf.py`` file (your Pelican
settings file) to alter the behavior of the plugin.

If a value is given below, this represents the effective default value. If no
value is given, the effective default value is ``None``.

*Tasknotes* also auto-configures itself when possible.  If you need to manually
create the default configuration, you would need the following:

.. code-block:: python

   # pelicanconf.py

   # if PLUGINS is not defined on Pelican 4.5+, these plugins will autoload
   PLUGINS = [
       "minchin.pelican.readers.tasknotes",
       # others, as desired...
   ]

   # the rest of the your configuration file...

This documentation has to be manually updated. If the settings no longer match
the plugin's behavior, or a setting is missing from here, please open a ticket
on `GitHub
<https://github.com/MinchinWeb/minchin.pelican.readers.tasknotes/issues>`_.

.. use the ".. data::" directive here for Sphinx output, but on GitHub, that just causes everything to disappear

ARTICLE_ORDER_BY = "reverse-date"
   Sorting order for micro blog posts (also used for sorting posts generally);
   micro posts will be sorted among all posts. (Regular Pelican setting)
AUTHOR
    Default author for micro blog posts. Can be overwritten by the metadata at
    the top of individual posts. (Regular Pelican setting; you don't have to
    supply an author.)
TASKNOTES_APPEND_HASHTAGS = True
   Tags gets appended at the end of the tasknote "summary line" as hashtags.
   *#taggedyou*  Tags have the CSS class ``.tasknotes-post-tag`` applied, if
   you want to conditionally control their display or formatting.
TASKNOTES_CATEGORY = "tasks"
   Default category for your tasknotes. It could be overwritten by the
   metadata on top of individual posts.
TASKNOTES_FOLDER = "tasks"
   Folder containing your tasknotes, relative to your content root
   folder.
TASKNOTES_SAVE_AS = ARTICLE_SAVE_AS
   What to save the tasknote output file as. Defaults to using the same file
   structure as you are using for articles (aka "regular" posts). c.f.
   ``TASKNOTES_URL``.
TASKNOTES_SLUG = "task-{date:%Y%m%d%H%M}"
   The slug that will be used for micro blog posts. Eg. ``task-202307091701``.

   Note that Pelican expects slugs to be universally unique.
TASKNOTES_URL = ARTICLE_URL
   What URL to post the tasknote to. Defaults to using the same URL structure
   as you are using for articles (aka "regular" posts). c.f.
   ``TASKNOTES_SAVE_AS``.

Integration with Themes
-----------------------

For best support, you will need to modify your theme, or select a theme that
already supports *Tasknotes*, like my `Seafoam
<http://blog.minchin.ca/label/seafoam/>`_.

Some helpful notes:

- Tasknotes are considered ``Articles`` by Pelican, and will be included
  in the ``articles`` and ``dates`` "lists" provided by the templating engine.
- Tasknotes all have ``article.tasknote = True``.
- Tasknotes posts are added to the ``tasks`` category (by default).
- Generally, you'll want to show the rendered tasknote, but perhaps as
  "regular" (or body) text. The title is set manually, and is generally the
  todo item proper. In general, use the summary (``article.summary``) for a
  short entry where you might otherwise show the post title. The whole body
  (``article.content``) will add any additional text added to the "body" of the
  tasknote.
- Appended tags have the CSS class ``.tasknotes-post-tag`` applied.


Changelog
---------

`Changelog <https://github.com/MinchinWeb/minchin.pelican.readers.tasknotes/blob/master/CHANGELOG.rst>`_

Roadmap
-------

To avoid (too much) premature optimization, I've written the plugin based on
how I am using it locally. That said, Pull Requests (and Feature Requests)
based on different usecases are welcomed!

Known Issues
------------

- Processing relies on CommonMark (Markdown) reader, which means you probably
  have to use it for the rest of your site as well.
- Default slug processing means that you can't have two tasks created the same
  minutes (or Pelican will break).

.. Credits
