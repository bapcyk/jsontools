from jsontools import indent
from jsontools import utils


class Schema:
    def read(self, src):
        if hasattr(src, 'read'): src = src.read()
        blocks = indent.indentblocks(src.splitlines())
        blocks = self._expand_blocks(blocks)
        for b in blocks:
            print(b)

    def _expand_blocks(self, blocks):
        for blk in blocks:
            spl = utils.splitesc(blk.ln, sep=';', trim=True)
            for i, ln in enumerate(spl):
                if i == 0:
                    yield blk._replace(ln=ln)
                else:
                    yield indent.block(op='nop', cnt=0, ln=ln)

    @classmethod
    def generate(js):
        ''' Generates schema from JSON
        '''
        # TODO


sch = Schema()
with open('schema.jv', 'rt') as f:
    sch.read(f)
