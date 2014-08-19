import time
import tempfile
import unittest

import chag

TEST_CHANGELOG = """
=========
CHANGELOG
=========

1.0.0 (2014-08-16)
------------------

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
""".lstrip()

TEST_CHANGELOG_EMPTY = """
=========
CHANGELOG
=========

Next release
------------
""".lstrip()


class TestChangelog(unittest.TestCase):

    def test_parses_files(self):
        with tempfile.NamedTemporaryFile('r+') as f:
            f.write(TEST_CHANGELOG)
            f.seek(0)
            changelog = chag.Changelog(f)
            self.assertEqual(len(changelog.entries), 3)
            leading = "=========\nCHANGELOG\n=========\n\n"
            self.assertEqual(leading, changelog.leading_content)
            self.assertEqual(changelog.entries[0].version, '1.0.0')
            self.assertEqual(changelog.entries[0].contents, 'Some contents')
            self.assertEqual(changelog.entries[2].contents, '* Test')

    def test_parses_string(self):
        changelog = chag.Changelog(TEST_CHANGELOG)
        self.assertEqual(len(changelog.entries), 3)
        self.assertEqual(changelog.entries[0].version, '1.0.0')
        self.assertEqual(changelog.entries[0].contents, 'Some contents')
        self.assertEqual(changelog.entries[2].contents, '* Test')

    def test_gets_specific_tag(self):
        changelog = chag.Changelog(TEST_CHANGELOG)
        entry = changelog.get_version('1.0.0')
        self.assertEqual(entry.version, '1.0.0')
        self.assertEqual(entry.heading, '1.0.0 (2014-08-16)')
        self.assertEqual(entry.line, 4)
        self.assertEqual(entry.contents, 'Some contents')

    def test_handles_empty_tags(self):
        changelog = chag.Changelog(TEST_CHANGELOG_EMPTY)
        entry = changelog.entries[0]
        self.assertEqual(entry.contents, '')

    def test_throws_when_version_not_found(self):
        changelog = chag.Changelog(TEST_CHANGELOG)
        self.assertRaises(ValueError, lambda: changelog.get_version('100'))

    def test_casts_to_string(self):
        changelog = chag.Changelog(TEST_CHANGELOG)
        self.assertEqual(TEST_CHANGELOG, str(changelog))

    def test_entry_handles_current_date(self):
        changelog = chag.Changelog(TEST_CHANGELOG)
        changelog.entries[-1].heading = 'Foo ()'
        replacement = '(' + time.strftime('%Y-%m-%d') + ')'
        expected = 'Foo ' + replacement
        self.assertTrue(expected in str(changelog))
