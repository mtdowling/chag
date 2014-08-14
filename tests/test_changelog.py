import os

import click
import pytest
import unittest
from chag import changelog


CHANGELOGA = """
=========
CHANGELOG
=========

Next Release
------------

Some contents

0.2.0 (2014-08-11)
------------------

Hello

* a
* b
  c

0.1.0
-----

* Test

"""

CHANGELOGB = """
CHANGELOG
=========

0.0.1
-----

"""

class TestChangelog(unittest.TestCase):

    def test_ensures_file_is_valid(self):
        with pytest.raises(click.ClickException):
            next(changelog.get_tags([], '-'))


    def test_ensures_changelog_is_valid(self):
        with pytest.raises(click.ClickException):
            next(changelog.get_tags('foo', '-'))


    def test_ensures_yields_tags(self):
        iter = changelog.get_tags(CHANGELOGA, '-')
        assert(next(iter) == {'line_number': 5,
                              'tag': 'Next',
                              'full_heading': 'Next Release',
                              'contents': 'Some contents'})
        assert(next(iter) == {'line_number': 10,
                              'tag': '0.2.0',
                              'full_heading': '0.2.0 (2014-08-11)',
                              'contents': """Hello\n\n* a\n* b\n  c"""})
        assert(next(iter) == {'line_number': 19,
                              'tag': '0.1.0',
                              'full_heading': '0.1.0',
                              'contents': '* Test'})


    def test_gets_specific_tag(self):
        for match in [(5, 'latest'), (10, '0.2.0'), (19, '0.1.0')]:
            found = changelog.get_tag(CHANGELOGA, '-', match[1])
            assert(match[0] == found['line_number'])


    def test_handles_empty_tags(self):
        found = changelog.get_tag(CHANGELOGB, '-', '0.0.1')
        assert('0.0.1' == found['full_heading'])
        assert('0.0.1' == found['tag'])
        assert('' == found['contents'])


    def test_can_parse_files(self):
        path = os.path.realpath(__file__ + '/../../CHANGELOG.rst')
        with open(path, 'rb') as file:
            found = changelog.get_tag(file, '-', '0.0.1')
            assert(found['tag'] == '0.0.1')
            assert(found['contents'] == '* Initial release.')


if __name__ == '__main__':
    unittest.main()
