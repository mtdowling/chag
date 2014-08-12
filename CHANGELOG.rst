=========
CHANGELOG
=========

Next Release (TBD)
------------------

Adding new commands and changing how parsing works.

* Made ``TAG`` a required argument for ``parse`` and ``tag``.
* ``parse`` now only outputs the contents of the changelog entry to STDOUT.
* Added ``list`` and ``latest`` commands.
* Added an ``update`` command that can be used to update a CHANGELOG TBD
  heading with a new changelog entry.

0.1.0 (2014-08-11)
------------------

* Using ``set -e``
* Simplifying function names and error handling.

0.0.4 (2014-08-11)
------------------

* Using POSIX style regular expression to work with GNU grep.
* Added a ``--version`` option.
* Writing errors to STDERR.
* Added a bats test suite.

0.0.3 (2014-08-10)
------------------

* Added the ability to prepend a "v" to a tag.

0.0.2 (2014-08-10)
------------------

* Correcting ``--debug`` description.

0.0.1 (2014-08-10)
------------------

* Initial release.
