====
chag
====

chag stands for changelog tag. It creates annotated git tags based on a
changelog entry.

Usage
-----

parse
~~~~~

Parses a changelog entry.

::

    Usage: chag parse [OPTIONS] FILENAME [TAG]

    Options:
      --help    Displays this message.

    Arguments:
      FILENAME  Path to the changelog file to parse.
      TAG       Optional tag to parse. If no value is provided, then
                the latest tag will be parsed.

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

      > ./chag /path/to/CHANGELOG.md
      1.0.1 2014-12-25 /tmp/1.0.1-XXXX

      > ./chag /path/to/CHANGELOG.md 1.0.1
      1.0.1 2014-12-25 /tmp/1.0.1-XXXX

tag
~~~

Creates an annotated git tag from a changelog entry.

::

    Usage: chag tag [OPTIONS] FILENAME [TAG]

    Options:
      --help    Displays this message.
      --title   Optional title to use for the annotated tag description. When
                pushing releases to GitHub releases, GitHub uses the first line
                of a changelog entry as part of the title of a release. If your
                changelog does not have a summary as the first line then you might
                want to provide a summary manually to better display the title on
                GitHub's releases.

                Pass "{date}" to automatically fill in the date of the release
                as the description title.

    Arguments:
      FILENAME  Path to the changelog to parse
      TAG       Optional release tag entry to parse. If no value is
                specified, then the latest entry is tagged.

    Description:
      Parses a changelog entry for the given tag (or latest tag) and creates an
      annotated git tag based on the changelog entry.

