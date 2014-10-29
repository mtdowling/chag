====
chag
====

*chag* (pronounced ``'chag``) stands for "changelog tag". It allows you to
use your project's changelog as the canonical source of change data.

.. image:: https://travis-ci.org/mtdowling/chag.svg?branch=master
   :target: https://travis-ci.org/mtdowling/chag
   :alt: Build status

What does it do?
----------------

1. Parse the contents of a specific changelog entry by tag name.
2. Create annotated git tags based on a changelog entry.
3. List all available tag version numbers in a changelog.
4. Get the version number of the latest changelog entry in a changelog.
5. In-place update a WIP changelog entry with an actual version number.

Why use chag?
-------------

1. Use your hand-curated changelog file as the canonical source of change
   information that can be easily parsed and shared in other locations
   (e.g., annotated tags, GitHub releases, etc.).
2. By using annotated tags with changelog contents, you can use your GitHub
   releases atom feed to keep your users up to date on releases. Take a look at
   `chag's atom feed <https://github.com/mtdowling/chag/releases.atom>`_ for
   an example.
3. If you use `Travis CI's deploy feature <http://docs.travis-ci.com/user/deployment/releases/>`_
   to automatically deploy to GitHub releases, then the contents of your GitHub
   releases will mirror the contents of the corresponding changelog entry.
4. Helps to ensure your changelog is always up to date.

Workflow
--------

While you can use any of the commands of chag as needed, the recommended
chag workflow is:

1. As you develop changes, add to your changelog file under a changelog
   section titled ``Unreleased``.
2. As you develop features, append items to your changelog.
3. When your work is ready to be released, execute ``chag update X.Y.Z``
   to update the WIP changelog entry to an actual version number. Substitute
   ``X.Y.Z`` with the version of the next tagged release.
4. Review the changes and commit them.
5. Run ``chag tag `` to create an annotated git tag based on the most recent
   changelog entry found in your changelog file.

Installation
------------

chag is just a single bash script. You need to add it to your path in order to
use it. One easy installation method is through cURL using the following:

::

    curl -s https://raw.githubusercontent.com/mtdowling/chag/master/install.sh | bash

You can customize the install source, directory and profile using the
CHAG_DIR and CHAG_VERSION environment variables. The script will place chag
in /usr/local/bin by default.

You can also install chag by cloning the repository and placing it somewhere
in your path manually.

Changelog Format
----------------

chag uses the changelog format described by
`keepachangelog.com <http://keepachangelog.com>`_. You are free to include any
content before the first changelog entry in the file. Each changelog entry MUST
start with an H2 markdown string ``## ``, followed by the version number of the
entry. The contents of a changelog entry can be anything you'd like.

Example Changelog
~~~~~~~~~~~~~~~~~

::

    # CHANGELOG

    Any text can occur before the actual release not entries are found.

    ## Unreleased

    * I've been building up this release while developing.
    * This helps to ensure the changelog is up to date.

    ## 1.0.1 - 2014-09-10

    Optional description of the release notes.

    * Updated something or another.
    * Here is another bullet point.

    ## 1.0.1 - 2014-09-01

    * Some bullet point data.

See chag's `CHANGELOG.md <https://github.com/mtdowling/chag/blob/master/CHANGELOG.md>`_
file for more examples.

Usage
-----

::

    Usage: chag <command> [<options>] [<args>]

    Options:
      --help     Displays this message.
      --version  Displays the version number.

    Commands:
      contents   Get the contents of a changelog entry.
      entries    List all versions in a changelog file.
      latest     Get the latest tag in a changelog.
      tag        Create an annotated git tag based on a changelog entry.

contents
~~~~~~~~

Outputs the contents of a changelog entry.

::

    Usage: chag contents [--help] [--file <path>] [--tag <tag>]

    Outputs the contents of a changelog entry from a changelog file. If no
    --tag option is provided, then the top-most entry in the changelog is
    parsed.

    Options:
      --file     Path to changelog. Defaults to CHANGELOG.md
      --tag      Tag version string to parse. Defaults to the latest.
      --help     Displays this message.

tag
~~~

Creates an annotated git tag from a changelog entry.

::

    Usage: chag tag [--help] [--file <path>] [--addv] [-s|--sign] [-f|--force]

    Parses a changelog entry for the given tag and creates an annotated git
    tag based on the changelog entry.

    Options:
      --file      Path to changelog. Defaults to CHANGELOG.md
      --addv      Pass to prepend a "v" to the git tag (e.g., "v2.0.1")
      --sign|-s   Make a GPG-signed tag, using the default git e-mail address key.
      --force|-f  Delete an existing tag if present.
      --help      Displays this message.

latest
~~~~~~

Get the latest changelog entry version from a CHANGELOG.

::

    Usage: chag latest [--help] [--file <path>]

    Get the latest changelog entry version from a CHANGELOG.

    Options:
      --file    Path to changelog. Defaults to CHANGELOG.md
      --help    Displays this message.

entries
~~~~~~~

List the changelog versions available in a CHANGELOG.

::

    Usage: chag entries [--help] [--file <path>]

    Lists all of the version numbers in a changelog file, separated by new lines.

    Options:
      --file    Path to changelog. Defaults to CHANGELOG.md
      --help    Displays this message.

update
~~~~~~

Replaces the top-most changelog entry heading with the provided version number.

::

    Usage: chag update [--help] [--file <path>] TAG

    Updates the top-most changelog entry with the given version number in
    the header of the entry and updates the entry date.

    Options:
      --file    Path to changelog. Defaults to CHANGELOG.md
      --help    Displays this message.

    Arguments:
      TAG       Version number to set on the entry.
