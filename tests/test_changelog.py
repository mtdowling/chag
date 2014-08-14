import os
import tempfile
import time

import pytest
import unittest
import click
from click.testing import CliRunner
from chag import changelog, main

CHANGELOG = os.path.realpath(__file__ + '/../../CHANGELOG.rst')

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
        assert next(iter) == {'line_number': 5,
                              'tag': 'Next',
                              'full_heading': 'Next Release',
                              'contents': 'Some contents'}
        assert next(iter) == {'line_number': 10,
                              'tag': '0.2.0',
                              'full_heading': '0.2.0 (2014-08-11)',
                              'contents': """Hello\n\n* a\n* b\n  c"""}
        assert next(iter) == {'line_number': 19,
                              'tag': '0.1.0',
                              'full_heading': '0.1.0',
                              'contents': '* Test'}

    def test_gets_specific_tag(self):
        for match in [(5, 'latest'), (10, '0.2.0'), (19, '0.1.0')]:
            found = changelog.get_tag(CHANGELOGA, '-', match[1])
            assert match[0] == found['line_number']

    def test_handles_empty_tags(self):
        found = changelog.get_tag(CHANGELOGB, '-', '0.0.1')
        assert '0.0.1' == found['full_heading']
        assert '0.0.1' == found['tag']
        assert '' == found['contents']

    def test_can_parse_files(self):
        with open(CHANGELOG, 'rb') as file:
            found = changelog.get_tag(file, '-', '0.0.1')
            assert found['tag'] == '0.0.1'
            assert found['contents'] == '* Initial release.'

    def test_cli_gets_contents(self):
        runner = CliRunner()
        result = runner.invoke(main.contents, [CHANGELOG, '0.0.1'])
        assert result.exit_code == 0
        assert result.output.strip() == '* Initial release.'

    def test_cli_gets_latest(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.get, [file.name, 'latest'])
            assert result.exit_code == 0
            assert result.output.strip() == 'Next'

    def test_cli_gets_latest_with_json(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.get, [file.name, 'latest', '--json'])
            assert result.exit_code == 0
            assert '"full_heading": "Next Release"' in result.output
            assert '"tag": "Next"' in result.output
            assert '"line_number": 5' in result.output
            assert '"contents": "Some contents"' in result.output

    def test_cli_fails_when_not_found(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.get, [file.name, 'foo'])
            assert result.exit_code == 1
            assert 'tag "foo" not found' in result.output

    def test_cli_lists_tags(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.list, [file.name])
            expected = ['Next', '0.2.0', '0.1.0']
            assert result.exit_code == 0
            assert result.output.split("\n")[:-1] == expected

    def test_cli_updates_latest(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.update, [file.name, 'Foo!'])
            assert result.exit_code == 0
            assert 'Updated first changelog entry to Foo!' in result.output
            file.seek(0)
            lines = file.readlines()
            assert lines[5] == "Foo!\n"
            assert lines[6] == "----\n"

    def test_cli_updates_latest_with_date(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.update, [file.name, '2.0.0 ()'])
            assert result.exit_code == 0
            expected = 'to 2.0.0 (%s)' % time.strftime('%Y-%m-%d')
            assert expected in result.output

    def test_cli_does_not_tag_latest(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(CHANGELOGA)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.tag, [file.name])
            assert result.exit_code == 1
            assert 'Not tagging a "Next Release" entry!' in result.output


if __name__ == '__main__':
    unittest.main()
