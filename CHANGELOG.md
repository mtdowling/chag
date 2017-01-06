# CHANGELOG

## 1.1.4 - 2017-01-06

* Fixed a problem with GNU grep where `chag contents` was unable to find
  entries.
* Now vendoring bats when testing.

## 1.1.3 - 2015-05-29

* Fixed an issue when searching for a tag using grep was matching tags that
  started with the same number. This could cause issues when you have tags
  like `3.0.0` and `3.0.0-beta.1`. Searching for tags now uses a more exact
  search in order to prevent these types of collisions.

## 1.1.2 - 2015-05-19

* Fixed an issue where searching for a tag using grep was matching dots as a
  regular expression dot, which provided false positives. Dots in tag names
  are now escaped when searching for tags.

## 1.1.1 - 2015-02-15

* Auto-detect CHANGELOG and CHANGELOG.md when no `--file` is provided.
* Adding missing `update` usage information to `chag --help`.

## 1.1.0 - 2014-10-28

* Removed the `--debug` option from the tag command.
* Removed the `--notrim` option from the contents command.
* Simplified a great deal and updated docs.

## 1.0.0 - 2014-10-26

* Using the format from http://keepachangelog.com
* Trimming down the feature set and switching back to bash instead of Python.
  This makes chag much simpler to install and does not require any
  dependencies.
* Simplified by removing `chag new`, `chag append`, and `chag get`.

## 0.5.0 - 2014-08-16

* Refactored to use classes and cleaned up implementation
* Added a ``new`` command used to create a ``Next Release`` entry.

## 0.4.0 - 2014-08-15

Python 3 compatibility

## 0.3.0 - 2014-08-14

Rewritten in Python using Click.

* Added the `append` command.
* Added the ability to get messages from an external editor.
* Added the ability to link Github issues and git commits.

## 0.2.0 - 2014-08-11

Adding new commands and changing how parsing works.

* Made ``TAG`` a required argument for ``parse`` and ``tag``.
* ``parse`` now only outputs the contents of the changelog entry to STDOUT.
* Added ``list`` and ``latest`` commands.
* Added an ``update`` command that can be used to update a CHANGELOG TBD
  heading with a new changelog entry.

## 0.1.0 - 2014-08-11

* Using ``set -e``
* Simplifying function names and error handling.

## 0.0.4 - 2014-08-11

* Using POSIX style regular expression to work with GNU grep.
* Added a ``--version`` option.
* Writing errors to STDERR.
* Added a bats test suite.

## 0.0.3 - 2014-08-10

* Added the ability to prepend a "v" to a tag.

## 0.0.2 - 2014-08-10

* Correcting ``--debug`` description.

## 0.0.1 - 2014-08-10

* Initial release.
