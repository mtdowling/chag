import json as j
import subprocess
import tempfile
import textwrap
import os

import click
import chag


def __load(f):
    """Loads the provided file or attempts to find the changelog file"""
    if f:
        return f
    for check in ['CHANGELOG', 'CHANGELOG.md', 'CHANGELOG.rst']:
        check = os.getcwd() + '/' + check
        if os.path.isfile(check):
            return open(check, 'r+')
    raise click.ClickException('Changelog file could not be found')


def __validate_changelog(changelog):
    if len(changelog.entries) == 0:
        raise click.ClickException('No changelog entries found in file')
    return changelog


def __get_message(m):
    if not m:
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmp:
            subprocess.call([os.environ.get('EDITOR', 'vim'), tmp.name])
            m = open(tmp.name, 'r').read()[:-1]
    return m


def __get_version(changelog, version):
    try:
        return changelog.get_version(version)
    except ValueError as e:
        raise click.ClickException(str(e))


@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-t', help='Tag version to retrieve', default='latest')
def contents(t, f, border):
    """Returns the changelog contents for the provided -t tag, or the latest
    tag if no -t option is provided.

    \b
    Examples:
      chag contents
      chag contents -t 0.1.0
      chag contents -f CHANGELOG -t latest
      chag contents --border='='
    """
    f = __load(f)
    changelog = __validate_changelog(chag.Changelog(f, border))
    entry = __get_version(changelog, t)
    click.echo(entry.contents)


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('--json/--no-json', default=False,
              help='Determines if JSON or just the version is returned.')
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-t', help='Tag version to retrieve', default='latest')
def get(t, f, border, json):
    """Prints out a specific tag number or JSON data for a specific tag. Pass
    'latest' as the -t option to parse the first found tag entry in the
    changelog.

    This command outputs JSON data when the --json option is provided. The
    JSON output contains the following keys:

    \b
    - line: Line that the tag heading is found
    - heading: The full heading line
    - version: Just the tag from the heading (e.g., '0.1.0')
    - contents: The text content of the changelog entry

    Examples:
      chag get -f CHANGELOG latest
      chag get --border='=' latest
      chag get --json 0.0.1
    """
    f = __load(f)
    changelog = __validate_changelog(chag.Changelog(f, border))
    entry = __get_version(changelog, t)
    if not json:
        click.echo(entry.version)
    else:
        click.echo(j.dumps({'line': entry.line,
                            'contents': entry.contents,
                            'heading': entry.heading,
                            'version': entry.version}))


@main.command()
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('--border', default='-', help='Repeated border character')
def entries(f, border):
    """Lists the tag versions available in a changelog file.

    \b
    Examples:
      chag list -f CHANGELOG
      chag list --border='='
    """
    f = __load(f)
    changelog = chag.Changelog(f, border)
    for entry in changelog.entries:
        click.echo(entry.version)


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-m', help='Heading to apply to the changelog')
def update(m, f, border):
    """Replaces the latest changelog entry with the provided -m message. If no
    -m option is provided, an editor will open where you can enter the
    changelog heading. The editor that is opened is based on the $EDITOR
    environment variable. If the last two characters of the provided heading
    are '()', they will be converted to today's date formatted as
    '(YYYY-MM-DD)'.

    \b
    Examples:
      chag update -f CHANGELOG.rst -m '1.0.1'
      chag update -m '1.0.1 ()'
      chag update --border='='
    """
    f = __load(f)
    changelog = __validate_changelog(chag.Changelog(f, border))
    changelog.entries[0].heading = __get_message(m)
    with open(f.name, 'w') as output:
        output.write(str(changelog))
    click.echo('Updated first changelog entry', err=True)
    click.echo("\n" + chag.git.diff(f.name), err=True)


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('--github', help='Pass the "user/repo" of your GitHub project')
@click.option('--wrap/--no-wrap', help='Wrap at 80 chars', default=True)
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-m', help='Changelog entry to append')
def append(f, border, github, m, wrap):
    """Appends an entry to the first changelog entry. Pass the entry in the
    -m option. If no -m option is provided, an editor will open where you can
    enter the changelog message to append. The editor that is opened is based
    on the $EDITOR environment variable.

    \b
    Examples:
        chag append -m '* Updated this file'
        chag append --github user/repo -m '* Updated this file'
        chag append --github user/repo --border='=' -m '* Updated this file'
        chag append
    """
    f = __load(f)
    changelog = __validate_changelog(chag.Changelog(f, border))
    m = __get_message(m)
    if github:
        m = chag.git.github_markdown(github, m)
    if wrap:
        m = "\n".join(textwrap.wrap(m, 80))
    changelog.entries[0].contents += "\n" + m
    with open(f.name, 'w') as output:
        output.write(str(changelog))
    click.echo('Appended to the first changelog entry', err=True)
    click.echo("\n" + chag.git.diff(f.name), err=True)


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('-f', type=click.File('r'), help='Path to changelog')
def new(f, border):
    """Create a "Next Release" changelog entry at the top of the changelog.

    \b
    Examples:
        chag new
        chag new --border '=' -f CHANGELOG.markdown
    """
    f = __load(f)
    changelog = chag.Changelog(f, border)
    changelog.entries.insert(0, chag.Entry(0, 'Next Release', '-', ''))
    with open(f.name, 'w') as output:
        output.write(str(changelog))
    click.echo('Created a new "Next Release" entry in changelog', err=True)
    click.echo("\n" + chag.git.diff(f.name), err=True)


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('--v-prefix/--no-v-prefix', default=False)
@click.option('--sign/--no-sign', default=False)
@click.option('--force/--no-force', default=False)
@click.option('-f', type=click.File('r'), help='Path to changelog')
def tag(f, border, v_prefix, sign, force):
    """Creates an annotated git tag from the latest changelog entry. The tag
    uses the version number found in the changelog entry's header line and the
    contents of the changelog entry as the tag annotation.

    \b
    Examples:
      chag tag -f /path/to/CHANGELOG.md
      chag tag --v-prefix
      chag tag --sign
      chag tag --force
      chag tag --debug
    """
    f = __load(f)
    changelog = __validate_changelog(chag.Changelog(f, border))
    found = changelog.entries[0]
    if found.version == 'Next':
        raise click.ClickException('Not tagging a "Next Release" entry!')
    click.echo('Ensuring git repository is clean with git diff', err=True)
    chag.git.is_clean()
    if v_prefix:
        tag_name = 'v' + found.version
    else:
        tag_name = found.version
    click.echo("Using the following annotation:", err=True)
    click.echo("============", err=True)
    click.echo(found.contents, err=True)
    try:
        chag.git.tag(tag_name, found.contents, force, sign)
        click.echo("============\nTagged %s" % tag_name, err=True)
    except Exception as e:
        raise click.ClickException(str(e))


if __name__ == '__main__':
    main()
