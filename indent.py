from collections import namedtuple


class IndentError(Exception):
    pass


def strindent(s, tabstep=None):
    """ Returns pair: (indent, valuable string):
    indent as number of spaces/tabs, if no tabstep,
    else number of steps (with width=tabstep). If
    indentation is odd, raise IndentError. If tabs
    and spaces are mixed - raises too. """
    parts = None
    tabs = spaces = False
    for i, ch in enumerate(s):
        if ch not in (' ', '\t'):
            parts = [s[:i], s[i:]]
            break
        elif ch == ' ':
            spaces = True
        elif ch == '\t':
            tabs = True
    if not parts:
        # no spaces/tabs in begin
        return [0, s]
    else:
        # found some spaces/tabs
        if tabs and spaces:
            # spaces and tabs are mixed!
            raise IndentError(r"mixed ' ', '\t' in indent")
        else:
            # good indent
            if not tabstep:
                return [len(parts[0]), parts[1]]
            else:
                if len(parts[0]) % tabstep:
                    raise IndentError('not odd indentation steps')
                else:
                    return [len(parts[0])//tabstep, parts[1]]


def indentlines(lines):
    """ Generator of indent. lines, yields pairs (level, string).
    First level is 0 """
    tabstep = None
    prevlev = 0
    for i, ln in enumerate(lines):
        if not ln.strip():
            # skip empty lines
            continue
        try:
            parts = strindent(ln, tabstep)
            if not tabstep and parts[0]:
                # first indent found, so it will be tabstep value
                tabstep = parts[0]
                parts[0] = 1
            if parts[0] - prevlev > 1:
                # indent may be 'deeper' only by 1 level!
                raise IndentError("unexpected indentation")
            yield parts
            prevlev = parts[0]
        except IndentError as x:
            raise IndentError("line %d: %s" % (i + 1, x))


def indentblocks(lines):
    block = namedtuple('Block', 'op cnt ln')
    prevlev = 0
    for lev, ln in indentlines(lines):
        if lev > prevlev:
            yield block('enter', 1, ln)
        elif lev == prevlev:
            yield block('nop', 0, ln)
        else:  # lev < prevlev:
            yield block('exit', prevlev - lev, ln)
        prevlev = lev


with open('schema.jv', 'rt') as f:
    for b in indentblocks(f.read().splitlines()):
        print(b)
