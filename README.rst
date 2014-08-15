====
chag
====

*chag* stands for "changelog tag". It allows you to use your project's
changelog as the canonical source of change data.

.. image:: https://travis-ci.org/mtdowling/chag.svg?branch=master
   :target: https://travis-ci.org/mtdowling/chag
   :alt: Build status

What does it do?
----------------

1. Parse the contents of a specific changelog entry by tag name.
2. Create annotated git tags based on a changelog entry.
3. List all available tag version numbers in a changelog.
4. Get the tag number of the latest changelog entry in a changelog.
5. In-place update a WIP changelog entry with an actual version number.
6. Easily append to the latest changelog entry with support for automatic issue
   and commit linking.

Why use chag?
-------------

1. Your project's GitHub releases atom feed contains release notes that can be
   used to keep consumers of your project up to date. Take a look at
   `chag's atom feed <https://github.com/mtdowling/chag/releases.atom>`_ for
   an example.
2. If you use `Travis CI's deploy feature <http://docs.travis-ci.com/user/deployment/releases/>`_
   to automatically deploy to GitHub releases, then the contents of your GitHub
   releases will mirror the contents of the corresponding changelog entry.
3. Helps to ensure your changelog is always up to date.

Workflow
--------

While you can use any of the commands of chag as needed, the recommended
chag workflow is:

1. As you develop changes, add to your changelog file under a changelog
   section titled ``Next Release``.
2. As you develop features, append items to your changelog using
   ``chag append``.
3. When your work is ready to be released, execute
   ``chag update -m 'X.Y.Z ()'`` where X.Y.Z is the version of the
   next tagged release and ``()`` is expanded to the current date. This
   command updates the "Next Release" entry in place with the new version
   number and date.
4. Review the changes and commit them.
5. Run ``chag tag `` to create an annotated git tag for the latest version.

Installation
------------

::

    pip install chag

Changelog Format
----------------

chag expects changelog files to match the following template:

1. Any number of lines can precede the start of the actual changelog entries
   (e.g., title, description of the file, etc.).
2. Each changelog entry MUST start with a heading line that can take any form.
3. After each heading line is a border line (a continuous number of repeated
   characters used to demarcate headings in markdown or reStructuredText),
   followed by another empty new line. The border line must be the same length
   as the preceding heading line.
4. Next is the changelog content. This can be any free-form text. chag will
   consume the content until the heading regular expression matches the
   next entry or the end of the file.

Example Changelog
~~~~~~~~~~~~~~~~~

::

    =========
    CHANGELOG
    =========

    Any text can occur before the actual release not entries are found.

    Next Release
    ------------

    * I've been building up this release while developing.
    * This helps to ensure the changelog is up to date.

    1.0.1 (2014-09-10)
    ------------------

    Optional description of the release notes.

    * Updated something or another.
    * Here is another bullet point.

    1.0.1 (2014-09-01)
    ------------------

    * Some bullet point data.

See chag's `CHANGELOG.rst <https://github.com/mtdowling/chag/blob/master/CHANGELOG.rst>`_
file for more examples.
