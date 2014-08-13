import re


def get_tag(lines, tag, border):
    """Get a specific tag entry by version number.

    Parameters
    ----------

    lines : a file object or iterable lines of a changelog.
    tag : str Specific tag to retrieve. Use 'latest' as the tag to return the
          first entry in the changelog.
    border : str The border character that is repeated under a tag.

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
    for found in get_tags(lines, border):
        if found['tag'] == tag or tag == 'latest':
            return found
    raise Exception('tag not found')


def get_tags(lines, border):
    """Yields each found tag from a changelog file.

    Parameters
    ----------

    lines : a file object or iterable lines of a changelog.
    border : str The border character that is repeated under a tag.

    Returns
    -------

    generator
        Each yielded item is a dictionary containing keys described in
        the get_tag() function.
    """
    if hasattr(lines, 'readlines'):
        lines = lines.readlines()
    last_line = len(lines) - 1
    regex = _get_regex(border)
    n = -1
    current = None

    for line in lines:
        n = n + 1
        if n == last_line:
            if current:
                current['contents'] = current['contents'] + line
                yield _clean_current(current)
        elif _is_heading(line, lines[n + 1], regex):
            if current:
                yield _clean_current(current)
            current = {
                'line_number': n,
                'full_heading': line.strip(),
                'tag': line.split(' ')[0],
                'contents': ''
            }
        elif current and not regex.match(line):
            current['contents'] = current['contents'] + line


def _clean_current(current):
    current['contents'] = current['contents'].strip()
    return current


def _get_regex(border):
    return re.compile('^' + re.escape(border) + '+$')


def _is_heading(line, next_line, regex):
    return regex.match(next_line) and len(line) == len(next_line)
