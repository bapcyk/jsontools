
NDEBUG = 0


def prn(*args, **kwargs):
    if not NDEBUG: print(*args, **kwargs)


def surrwith(s, c, paired=True):
    if paired:
        c1 = c
        c2 = {'(': ')', '[': ']', '{': '}', '<': '>'}.get(c1, c1)
    else: c1 = c2 = c
    return s.startswith(c1) and s.endswith(c2)


def atom(s):
    if surrwith(s, '"') or surrwith(s, "'"): return s[1:-1]
    else:
        try: return int(s)
        except:
            try: return float(s)
            except: raise ValueError("invalid literal (str, int, float): '%s'" % s)


def values(obj):
    if isinstance(obj, dict):
        yield from obj.values()
    elif isinstance(obj, (list, tuple)):
        yield from obj


def safe_eval(expr, *args, default=None):
    try: return eval(expr, *args)
    except: return default


class Query:
    THEN = '/'
    WHERE = '|'

    def __init__(self, obj):
        self.root = obj

    def _iter_from_one(self, obj, sel):
        if sel == '*':
            yield from values(obj)
        elif sel == '**':
            for obj in values(obj):
                yield obj
                yield from self._iter_from_one(obj, sel)
        elif sel == '':
            yield obj
        else:
            idx = atom(sel)
            try: yield obj[idx]
            except: pass

    def _sel_from_one(self, obj, sel):
        sel, *cond = sel.split(self.WHERE)
        if cond:
            cond = cond[0].replace('$', 'obj')
            for obj in self._iter_from_one(obj, sel):
                allowed = safe_eval(cond, globals(), locals())
                if allowed: yield obj
        else:
            yield from self._iter_from_one(obj, sel)

    def _sel_from_all(self, objs, sel):
        for obj in objs:
            prn('obj', obj)
            yield from self._sel_from_one(obj, sel)

    def _sel(self, objs, sels):
        if not sels:
            yield from objs
        else:
            sel = sels[0]
            objs = self._sel_from_all(objs, sel)
            prn('objs', objs, sel)
            yield from self._sel(objs, sels[1:])

    def _do(self, expr):
        yield from self._sel([self.root], expr.split(self.THEN))

    __call__ = _do


###############################################################################
nassert = -1


def assert_query(obj, expr, exp):
    global nassert
    nassert += 1
    query = Query(obj)
    exp = list(exp)
    for res in query(expr):
        assert res in exp, "%d: %s not expected" % (nassert, res)
        exp.remove(res)
    assert not exp, "%d: missed: %s" % (nassert, exp)


if __name__ == '__main__':
    NDEBUG = 1
    data = {1: {'a': [10, {'x': [33, 34, 35, 36]}, 30, 40],
                'b': 'bbb'
                },
            2: [0, {1: {'x': 'XYZ'}}]}
    prn('RESULT:')
    # query = Query(data)
    q1 = '**/"x"'
    q2 = '2/1/1/"x"'
    q3 = '*/1'
    q4 = '*/*'
    q5 = '1/"a"/1/"x"/*|$%2'

    # for res in query(q5):
    #     print("  res:", res)

    assert_query(data, q1, [[33, 34, 35, 36], 'XYZ'])
    assert_query(data, q2, ['XYZ'])
    assert_query(data, q3, [{1: {'x': 'XYZ'}}])
    assert_query(data, q4, [[10, {'x': [33, 34, 35, 36]}, 30, 40], 'bbb', 0, {1: {'x': 'XYZ'}}])
    assert_query(data, q5, [33, 35])
