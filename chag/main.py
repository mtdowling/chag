import json as j
import subprocess
import tempfile
import os

import click
import changelog
import chag.git as git


def _load_changelog(f):
    """Loads the provided file or attempts to find the changelog file"""
    if f:
        return f
    for check in ['CHANGELOG', 'CHANGELOG.md', 'CHANGELOG.rst']:
        check = os.getcwd() + '/' + check
        if os.path.isfile(check):
            return open(check, 'r+')
    raise click.ClickException('Changelog file not provided and not found')


def _get_message(m):
    """Gets a message from a variable or EDITOR if not set"""
    if not m:
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tmp:
            subprocess.call([os.environ.get('EDITOR', 'vim'), tmp.name])
            m = open(tmp.name, 'r').read()[:-1]
    return m


@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-t', help='Tag to retrieve', default='latest')
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
    f = _load_changelog(f)
    click.echo(changelog.get_tag(f, border, t)['contents'])


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('--json/--no-json', default=False,
              help='Determines if JSON or just the version is returned.')
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-t', help='Tag to retrieve', default='latest')
def get(t, f, border, json):
    """Prints out a specific tag number or JSON data for a specific tag. Pass
    'latest' as the -t option to parse the first found tag entry in the
    changelog.

    This command outputs JSON data when the --json option is provided. The
    JSON output contains the following keys:

    \b
    - line_number: Line that the tag heading is found
    - full_heading: The full heading line
    - tag: Just the tag from the heading (e.g., '0.1.0')
    - contents: The text content of the changelog entry

    Examples:
      chag get -f CHANGELOG latest
      chag get --border='=' latest
      chag get --json 0.0.1
    """
    f = _load_changelog(f)
    if json:
        click.echo(j.dumps(changelog.get_tag(f, border, t)))
    else:
        click.echo(changelog.get_tag(f, border, t)['tag'])


@main.command()
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('--border', default='-', help='Repeated border character')
def list(f, border):
    """Lists the tag versions available in a changelog file.

    \b
    Examples:
      chag list -f CHANGELOG
      chag list --border='='
    """
    for tag in changelog.get_tags(_load_changelog(f), border):
        print(tag['tag'])


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
    heading = _get_message(m)
    heading = changelog.update(_load_changelog(f), border, heading)
    click.echo('Updated first changelog entry to %s' % heading, err=True)


@main.command()
@click.option('--border', default='-', help='Repeated border character')
@click.option('--github', help='Pass the "user/repo" of your GitHub project')
@click.option('-f', type=click.File('r'), help='Path to changelog')
@click.option('-m', help='Changelog entry to append')
def append(f, border, github, m):
    """Appends an entry to the first changelog entry. Pass the entry in the
    -m option. If no -m option is provided, an editor will open where you can
    enter the changelog message to append. The editor that is opened is based
    on the $EDITOR environment variable.

    \b
    Examples:
        chag append -m '* Updated this file'
        chag append --github -m '* Updated this file'
        chag append --github --border='=' -m '* Updated this file'
        chag append
    """
    m = _get_message(m)
    if github:
        m = git.github_markdown(github, m)
    changelog.append(_load_changelog(f), border, m)
    click.echo('Appended to the first changelog entry:', err=True)
    click.echo(m, err=True)


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
    f = _load_changelog(f)
    found = changelog.get_tag(f, border, 'latest')
    if found['tag'] == 'Next':
        raise click.ClickException('Not tagging a "Next Release" entry!')
    click.echo('Ensuring git repository is clean with git diff', err=True)
    git.is_clean()
    if v_prefix:
        tag_name = 'v' + found['tag']
    else:
        tag_name = found['tag']
    click.echo("Using the following annotation:", err=True)
    click.echo('  ' + found['contents'].replace("\n", "\n    "), err=True)
    try:
        git.tag(tag_name, found['contents'], force, sign)
        click.echo('[SUCCESS] Tagged %s' % tag_name, err=True)
    except Exception as e:
        raise click.ClickException('[FAILED] %s' % str(e))


if __name__ == '__main__':
    main()
