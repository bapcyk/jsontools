import re


MISS = object()

def surrwith(s, c, paired=True):
    if paired:
        c1 = c
        c2 = {'(': ')', '[': ']', '{': '}', '<': '>'}.get(c1, c1)
    else: c1 = c2 = c
    return s.startswith(c1) and s.endswith(c2)


def values(seq):
    if isinstance(seq, dict):
        yield from seq.values()
    elif isinstance(seq, (list, tuple)):
        yield from seq
    elif isinstance(seq, (str, bytes)):
        yield from seq


def first(seq, default=MISS):
    args = (values(seq),) + () if default is MISS else (None,)
    return next(*args)


def safe_eval(expr, *args, default=None):
    try: return eval(expr, *args)
    except: return default


def getitem(obj, item, default=None):
    try: return obj[item]
    except (KeyError, IndexError): return default


def splitesc(string, sep, trim=True):
    ''' Split string by `sep` and `trim` it if need. To escape
    `sep` double one are used:
    >>> splitesc('aaa;;1;bbb ; ccc ', ';', True)
    ['aaa;1', 'bbb', 'ccc']
    '''
    unesc = lambda s: s.replace(2*sep, sep)
    rexp = '(?<!{0}){0}(?!{0})'.format(sep)
    fnd = re.split(rexp, string)
    if not trim: return fnd
    else:
        return [unesc(s) for s in map(str.strip, fnd) if s]
