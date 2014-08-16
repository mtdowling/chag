import os
import tempfile
import time
import shutil
import subprocess
import unittest

import chag
from chag import main
from click.testing import CliRunner

CHANGELOG = os.path.realpath(__file__ + '/../../CHANGELOG.rst')

TEST_CHANGELOG = """
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
""".lstrip()


class TestCli(unittest.TestCase):

    def __create_git(self, changelog):
        """Initializes a git repository"""
        self.__cleanup_git()
        self.dir = tempfile.mkdtemp()
        os.chdir(self.dir)
        self.f = self.dir + '/CHANGELOG'
        with open(self.f, 'w') as f:
            f.write(changelog)
        subprocess.check_call(['git', 'init'], stdout=subprocess.PIPE)
        subprocess.check_call(['git', 'add', '-A'], stdout=subprocess.PIPE)
        subprocess.check_call(['git', 'commit', '-m', 'Test'],
                              stdout=subprocess.PIPE)

    def __cleanup_git(self):
        """Deletes the test git repository if needed"""
        if hasattr(self, 'dir') and len(self.dir):
            shutil.rmtree(self.dir)

    def tearDown(self):
        self.__cleanup_git()

    def test_cli_gets_contents(self):
        runner = CliRunner()
        result = runner.invoke(main.contents, ['-f', CHANGELOG,
                                               '-t', '0.0.1'])
        assert result.exit_code == 0
        assert result.output.strip() == '* Initial release.'

    def test_cli_gets_latest(self):
        with tempfile.NamedTemporaryFile('w+') as file:
            file.write(TEST_CHANGELOG)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.get, ['-f', file.name])
            assert result.exit_code == 0
            assert result.output.strip() == 'Next'

    def test_cli_gets_latest_with_json(self):
        with tempfile.NamedTemporaryFile('w+') as file:
            file.write(TEST_CHANGELOG)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.get, ['-f', file.name, '--json'])
            assert result.exit_code == 0
            assert '"heading": "Next Release"' in result.output
            assert '"version": "Next"' in result.output
            assert '"line": 4' in result.output
            assert '"contents": "Some contents"' in result.output

    def test_cli_fails_when_not_found(self):
        with tempfile.NamedTemporaryFile('w+') as file:
            file.write(TEST_CHANGELOG)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(chag.main.get, ['-f', file.name,
                                                   '-t', 'foo'])
            assert result.exit_code == 1
            assert 'Version foo not found' in result.output
            assert 'Must be a valid version' in result.output

    def test_cli_lists_entries(self):
        with tempfile.NamedTemporaryFile('w+') as file:
            file.write(TEST_CHANGELOG)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.entries, ['-f', file.name])
            assert result.exit_code == 0
            expected = ['Next', '0.2.0', '0.1.0']
            assert result.output.split("\n")[:-1] == expected

    def test_cli_updates_latest(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.update, ['-f', self.f,
                                             '-m', 'Foo!'])
        assert result.exit_code == 0
        assert 'Updated first changelog entry' in result.output
        with open(self.f, 'r') as f:
            lines = f.readlines()
            assert lines[4] == "Foo!\n"
            assert lines[5] == "----\n"

    def test_cli_updates_latest_with_date(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.update, ['-f', self.f,
                                             '-m', '2.0.0 ()'])
        assert result.exit_code == 0
        with open(self.f, 'r') as f:
            lines = f.readlines()
            expected = "2.0.0 (%s)\n" % time.strftime('%Y-%m-%d')
            assert lines[4] == expected

    def test_cli_appends_to_latest(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.append, ['-f', self.f,
                                             '-m', 'Hello!'])
        assert result.exit_code == 0
        with open(self.f, 'r') as f:
            lines = f.readlines()
            assert lines[8] == "Hello!\n"

    def test_cli_appends_to_latest_with_github(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.append, ['-f', self.f,
                                             '-m', 'Issue #2, abeffff',
                                             '--github', 'foo/bar'])
        assert result.exit_code == 0
        with open(self.f, 'r') as f:
            lines = f.readlines()
            expected = "Issue https://github.com/foo/bar/issues/2, abeffff\n"
            assert lines[8] == expected

    def test_cli_creates_new_entry(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.new, ['-f', self.f])
        assert result.exit_code == 0
        with open(self.f, 'r') as f:
            lines = f.readlines()
            assert lines[4] == "Next Release\n"
            assert lines[5] == "------------\n"
            assert lines[6] == "\n"
            assert lines[7] == "\n"
            assert lines[8] == "\n"

    def test_cli_does_not_tag_latest(self):
        with tempfile.NamedTemporaryFile('w+') as file:
            file.write(TEST_CHANGELOG)
            file.seek(0)
            runner = CliRunner()
            result = runner.invoke(main.tag, ['-f', file.name])
            assert result.exit_code == 1
            assert 'Not tagging a "Next Release" entry!' in result.output

    def test_cli_tag_ensures_git_is_clean(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.update, ['-f', self.f, '-m', '2.0.0'])
        assert result.exit_code == 0
        result = runner.invoke(main.tag)
        assert result.exit_code == 1
        assert 'Your repository is not clean' in result.output

    def test_cli_tags_latest(self):
        self.__create_git(TEST_CHANGELOG)
        runner = CliRunner()
        result = runner.invoke(main.update, ['-f', self.f, '-m', '2.0.0'])
        assert result.exit_code == 0
        subprocess.check_call(['git', 'add', '-A'], stdout=subprocess.PIPE)
        subprocess.check_call(['git', 'commit', '-m', 'Updating changelog'],
                              stdout=subprocess.PIPE)
        result = runner.invoke(main.tag)
        assert result.exit_code == 0
        assert 'Tagged 2.0.0' in result.output
        p = subprocess.Popen(['git', 'tag', '-n1', '-l', '2.0.0'],
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        assert '2.0.0' in str(out)
        assert 'Some contents' in str(out)
