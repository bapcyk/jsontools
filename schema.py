from jsontools import indent
import re

# TODO values unescape (;; -> ;   etc)

def splitnodes(string, trim=True):
    fnd = re.split('(?<!;);(?!;)', string)
    if not trim: return fnd
    else:
        return [s for s in map(str.strip, fnd) if s]
