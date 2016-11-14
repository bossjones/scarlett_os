from __future__ import absolute_import, unicode_literals

import re
import unicodedata


def indent(string, places=4, linebreak='\n', singles=False):
    lines = string.split(linebreak)
    if not singles and len(lines) == 1:
        return string
    for i, line in enumerate(lines):
        lines[i] = ' ' * places + line
    result = linebreak.join(lines)
    if not singles:
        result = linebreak + result
    return result


def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.

    This function is based on Django's slugify implementation.
    """
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def capitalize(str):
    """Capitalize a string, not affecting any character after the first."""
    return str[:1].upper() + str[1:]

def _split_numeric_sortkey(s, limit=10,
                           reg=re.compile(r"[0-9][0-9]*\.?[0-9]*").search,
                           join=u" ".join):
    """Separate numeric values from the string and convert to float, so
    it can be used for human sorting. Also removes all extra whitespace."""
    result = reg(s)
    if not result or not limit:
        text = join(s.split())
        return (text,) if text else tuple()
    else:
        start, end = result.span()
        return (
            join(s[:start].split()),
            float(result.group()),
            _split_numeric_sortkey(s[end:], limit - 1))


def human_sort_key(s, normalize=unicodedata.normalize):
    if not s:
        return ()
    if not isinstance(s, text_type):
        s = s.decode("utf-8")
    s = normalize("NFD", s.lower())
    return _split_numeric_sortkey(s)


def make_case_insensitive(filename):
    return "".join(["[%s%s]" % (c.lower(), c.upper()) for c in filename])
