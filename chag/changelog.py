import re
import time


class Changelog(object):
    """Represents the contents of a changelog file"""

    def __init__(self, data, border='-'):
        self.leading_content = ''
        self.border = border
        self.entries = self.__parse(self.__normalize_input(data))

    def get_version(self, version):
        for entry in self.entries:
            if entry.version == version or version == 'latest':
                return entry
        valid_entries = [entry.version for entry in self.entries]
        raise ValueError('Version %s not found. Must be a valid version: %s'
                         % (version, valid_entries))

    def __str__(self):
        result = self.leading_content
        for entry in self.entries:
            result += str(entry) + "\n"
        return result.strip() + "\n"

    def __parse(self, lines):
        n = -1
        regex = re.compile('^' + re.escape(self.border) + '+$')
        entries = []

        while len(lines):
            line = lines.pop(0)
            n += 1
            if len(lines) and self.__heading(line, lines[0], regex):
                entries.append(Entry(n, line.strip(), self.border))
                # Skip the border line
                lines.pop(0)
                n += 1
            elif len(entries):
                entries[-1].contents += line
            else:
                self.leading_content += line

        # Remove extra spaces from each entry
        for entry in entries:
            entry.contents = entry.contents.strip()

        return entries

    @staticmethod
    def __normalize_input(data):
        if type(data) is str:
            # Split on "\n" but ensure each line still has a trailing "\n"
            lines = [l + "\n" for l in data.split("\n")]
        elif hasattr(data, 'readlines'):
            lines = data.readlines()
        else:
            raise ValueError('Invalid changelog supplied')
        if len(lines) < 2:
            raise ValueError('Not a valid changelog file')
        return lines

    @staticmethod
    def __heading(line, next_line, regex):
        return regex.match(next_line) and len(line) == len(next_line)


class Entry(object):
    """Represents a single changelog entry"""
    def __init__(self, line, heading, border='-', contents=''):
        self.heading = heading
        self.version = self.heading.split(' ')[0]
        self.contents = contents
        self.border = border
        self.line = line

    def __str__(self):
        heading = self.heading
        # Replace "()" with the current date
        if heading[-2::] == '()':
            replacement = '(' + time.strftime('%Y-%m-%d') + ')'
            heading = heading.replace('()', replacement)
        return "%s\n%s\n\n%s\n" % (heading,
                                   self.border * len(heading),
                                   self.contents.strip())
