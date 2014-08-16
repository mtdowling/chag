import re
import subprocess as sp
import tempfile

import click


def diff(filename=None):
    cmd = ['git', 'diff', '-u']
    if filename:
        cmd.append(filename)
    p = sp.Popen(cmd, stdout=sp.PIPE)
    out, err = p.communicate()
    return str(out)


def is_clean():
    """Ensures the git repository does not have any staged or changed files"""
    try:
        cmd = 'git diff --stat --exit-code'.split(' ')
        sp.check_call(cmd)
        cmd.append('--cached')
        sp.check_call(cmd)
    except sp.CalledProcessError:
        raise click.ClickException('Your repository is not clean')


def is_commit(sha):
    """Checks to see if the given sha matches a git commit"""
    child = sp.Popen(['git', 'show', sha, '--stat'],
                     stdout=sp.PIPE,
                     stderr=sp.PIPE)
    child.communicate()
    return child.returncode == 0


def github_markdown(repo, text):
    """Performs a subset of Github flavored markdown"""
    def _github_issues(repo):
        base_url = 'https://github.com/' + repo + '/issues/'
        return lambda match: base_url + match.group(1)

    def _git_commit(repo):
        base_url = 'https://github.com/' + repo + '/commit/'
        return lambda match: base_url + match.group(1) \
            if is_commit(match.group(1)) else match.group(1)

    text = re.sub("#(\d+)", _github_issues(repo), text)
    text = re.sub("([A-Fa-f0-9]{7})", _git_commit(repo), text)
    return text


def tag(name, contents, force=False, sign=False):
    """Creates an annotated git tag"""
    args = ['git', 'tag', '-a', '-F', '-']
    if force:
        args.append('--force')
    if sign:
        args.append('--sign')
    args.append(name)

    with tempfile.TemporaryFile('r+') as tmp:
        tmp.write(contents)
        tmp.seek(0)
        sp.check_call(args, stdin=tmp)
        return args
