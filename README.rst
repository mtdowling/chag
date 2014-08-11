====
chag
====

*chag* stands for "changelog tag". It allows you to use your project's
changelog as the canonical source of change data.

You can use chag to:

1. Create annotated git tags based on a changelog entry.
2. Parse a changelog into a tag name, date, and description.

Adding snippets of your changelog to annotated git tags provides the following
benefits:

1. Your project's GitHub releases atom feed contains release notes that can be
   used to keep consumers of your project up to date. Take a look at
   `chag's atom feed <https://github.com/mtdowling/chag/releases.atom>`_ for
   an example.
2. If you use `Travis CI's deploy feature <http://docs.travis-ci.com/user/deployment/releases/>`_
   to automatically deploy to GitHub eleases, then the contents of your GitHub
   releases will mirror the contents of the corresponding changelog entry.

.. image:: https://travis-ci.org/mtdowling/chag.svg?branch=master
   :target: https://travis-ci.org/mtdowling/chag
   :alt: Build status

Workflow
--------

Using "chag tag" requires the following workflow:

1. Create a changelog entry in your project's CHANGELOG file that contains the
   version to be released and information about the release.
2. Commit the CHANGELOG changes.
3. Run ``chag tag CHANGELOG`` (where CHANGELOG is the path to your changelog).


Installation
------------

To install you could use the install script using cURL:

::

    curl -s https://raw.githubusercontent.com/mtdowling/chag/master/install.sh | bash

You can customize the install source, directory and profile using the
CHAG_DIR and CHAG_VERSION environment variables. The script will place chag
in /usr/local/bin by default.

You can also install chag by cloning the repository and placing it somewhere
in your path manually.

Changelog Format
----------------

chag expects changelog files to match the following template:

1. Any number of lines can precede the start of the actual changelog entries
   (e.g., title, description of the file, etc.).
2. Each changelog entry MUST start with a header line that matches the
   following regular expression: ``\d+\.\d+\.\d+ \(\d{4}\-\d{2}\d{2}\)``.
   The first part of the pattern is the version number, and the second
   part of the pattern is the release date in the form of YYYY-MM-DD
   (or YYYY-DD-MM works as well).
3. After each header line is a border line (a continuous number of repeated
   characters used to demarcate headings in markdown or reStructuredText),
   followed by another empty new line.
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

Usage
-----

::

    Usage: chag [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Displays this message.

    Commands:
      parse
      tag

parse
~~~~~

Parses a changelog entry. If no ``--tag`` option is provided, then the latest
changelog entry is parsed.

::

    Usage: chag parse [OPTIONS] FILENAME

    Options:
      --tag      Optional tag to parse. If no value is provided, then
                 the latest tag will be parsed.
      --debug    Output debug information while executing.
      --help     Displays this message.

    Arguments:
      FILENAME   Path to the changelog file to parse.

    Description:
      Parses a changelog entry from a changelog file. A changelog
      file consists of various release entries, each designated by a line
      that matches the following pattern: '\d+\.\d+\.\d+ \(\d{4}\-\d{2}\d{2}\)'
      After each release entry heading, are two lines of text that are
      disregarded, followed by n number of lines of the changelog entry
      content. An entry is parsed until the next heading or EOF.

    Output:
      Outputs the tag of the corresponding entry, the date of the
      entry, and the path to a file on disk containing the contents
      of the entry, all separated by a single space.

    Examples:

      ./chag /path/to/CHANGELOG.md
      Outputs: 1.0.1 2014-12-25 /tmp/1.0.1-XXXX

      ./chag --tag 1.0.1 /path/to/CHANGELOG.md
      Outputs: 1.0.1 2014-12-25 /tmp/1.0.1-XXXX

tag
~~~

Creates an annotated git tag from a changelog entry. If no ``--tag`` option
is provided, then the latest changelog entry is parsed and tagged.

::

    Usage: chag tag [OPTIONS] FILENAME

    Options:
      --tag       Optional tag to parse. If no value is provided, then
                  the latest tag will be parsed. Defaults to "latest".
      --add-v     Pass to prepend a "v" to the git tag (e.g., "v2.0.1")
      --message   Optional message to prepend to the annotated tag description.
                  Pass "{date}" to automatically fill in the date of the release
                  as the description title.
      --sign|-s   Make a GPG-signed tag, using the default git e-mail address's
                  key.
      --force|-f  Delete an existing tag if present.
      --debug     Output debug information while executing.
      --help      Displays this message.

    Arguments:
      FILENAME   Path to the changelog to parse

    Description:
      Parses a changelog entry for the given tag (or latest tag) and creates an
      annotated git tag based on the changelog entry.

    Examples:
      ./chag tag /path/to/CHANGELOG.md
      ./chag tag --debug CHANGELOG.rst
      ./chag tag --tag 4.1.0 CHANGELOG.md
      ./chag tag --sign CHANGELOG.rst
      ./chag tag -s CHANGELOG.rst
      ./chag tag --force CHANGELOG.rst
      ./chag tag -f CHANGELOG.rst
      ./chag tag --message "{date}" CHANGELOG.rst
      ./chag tag --message "Release code name" CHANGELOG.rst

Executing ``chag tag`` will have output similar to the following:

::

    ./chag tag --debug CHANGELOG.rst
    Parsed the 0.0.1 changelog entry from CHANGELOG.rst:
      tag: 0.0.1, date: 2014-09-10, tmpfile: /var/folders/2d//T/tag-0.0.1.XXXXXXXXXX.QjNa2HSO
    Running git tag -a -F /var/folders/2d//T/tag-0.0.1.XXXXXXXXXX.QjNa2HSO
    [SUCCESS] Tagged the 0.0.1 release
    Tagged 0.0.1 with the following annotation:

    Initial release.
