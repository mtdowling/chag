import re
import time

import click


def get_tag(changlog, border, tag):
    """Get a specific tag entry by version number.

    Parameters
    ----------

    changelog : a file object or string of a changelog.
    border : str The border character that is repeated under a tag.
    tag : str Specific tag to retrieve. Use 'latest' as the tag to return the
          first entry in the changelog.

    Returns
    -------

    dictionary

        - line_number: Line that the tag heading is found
        - full_heading: The full heading line
        - tag: Just the tag from the heading (e.g., '0.1.0')
        - contents: The text content of the changelog entry

    Raises
    ------

    Exception
        If the tag cannot be found
    """
    for found in get_tags(changlog, border):
        if found['tag'] == tag or tag == 'latest':
            return found
    raise click.ClickException('tag "%s" not found' % tag)


def get_tags(changelog, border):
    """Yields each found tag from a changelog file.

    Parameters
    ----------

    changelog : a file object or string of a changelog.
    border : str The border character that is repeated under a tag.

    Returns
    -------

    generator
        Each yielded item is a dictionary containing keys described in
        the get_tag() function.
    """
    if type(changelog) is str:
        # Split on "\n" but ensure each line still has a trailing "\n"
        changelog = [l + "\n" for l in changelog.split("\n")]
    elif hasattr(changelog, 'readlines'):
        changelog = changelog.readlines()
    else:
        raise click.ClickException('Invalid changelog supplied')

    if len(changelog) < 2:
        raise click.ClickException('Not a valid changelog file')

    n = -1
    current = None
    last_line = len(changelog) - 1
    regex = re.compile('^' + re.escape(border) + '+$')

    for line in changelog:
        n += 1
        if n == last_line:
            if current:
                yield _clean_current(current, line)
        elif _is_heading(line, changelog[n + 1], regex):
            if current:
                yield _clean_current(current)
            current = {
                'line_number': n,
                'full_heading': line.strip(),
                'tag': line.strip().split(' ')[0],
                'contents': ''
            }
        elif current and not regex.match(line):
            current['contents'] += line


def update(changelog, border, heading):
    """Updates a specific entry in a changelog file.

    Parameters
    ----------

    changelog : a changelog file object
    border : str The border character that is repeated under a tag.
    heading : The heading to add to the first changelog item

    Return
    ------

    str
        Returns the string that was used as the heading in the entry.
    """
    # Replace the date if needed
    if heading[-2::] == '()':
        replacement = '(' + time.strftime('%Y-%m-%d') + ')'
        heading = heading.replace('()', replacement)
    found = get_tag(changelog, border, 'latest')
    changelog.seek(0)
    lines = changelog.readlines()
    lines[found['line_number']] = heading + "\n"
    lines[found['line_number'] + 1] = (border * len(heading)) + "\n"
    with open(changelog.name, 'w') as f:
        f.write(''.join(lines))
    return heading


def append(changelog, border, entry):
    """Appends an entry to the first changelog entry.

    Parameters
    ----------

    changelog : a changelog file object
    border : str The border character that is repeated under a tag.
    entry: str The entry to append.

    Return
    ------

    str
        Returns the entry that was appended.
    """
    tag = get_tag(changelog, border, 'latest')
    changelog.seek(0)
    lines = changelog.readlines()
    content_size = tag['contents'].count("\n")
    append_line = tag['line_number'] + 3 + content_size
    lines[append_line] += entry + "\n"

    with open(changelog.name, 'w') as f:
        f.write(''.join(lines))

    return entry


def _clean_current(current, line=None):
    if line:
        current['contents'] += line
    current['contents'] = current['contents'].strip()
    return current


def _is_heading(line, next_line, regex):
    return regex.match(next_line) and len(line) == len(next_line)
