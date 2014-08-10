====
chag
====

*chag* stands for "changelog tag". It creates annotated git tags based on a
changelog entry. You can also use chag simply to parse a changelog into a tag
name, date, and description.

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
-----------------

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

Parses a changelog entry.

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
      that matches the following pattern: \d+\.\d+\.\d+ \(\d{4}\-\d{2}\d{2}\)
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

Creates an annotated git tag from a changelog entry.

::

    Usage: chag tag [OPTIONS] FILENAME

    Options:
      --tag       Optional tag to parse. If no value is provided, then
                  the latest tag will be parsed. Defaults to "latest".
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
